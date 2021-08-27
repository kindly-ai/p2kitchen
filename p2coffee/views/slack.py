import json
from http import HTTPStatus
from pprint import pprint

import requests
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
from rest_framework.views import APIView

from p2coffee.models import Machine
from p2coffee.slack import verify_signature


class SlackCommandView(APIView):
    COMMANDS = ["status", "help"]

    def post(self, request):
        verify_signature(request)
        """
        Handle slack command payloads.
        Ref: https://api.slack.com/interactivity/slash-commands#app_command_handling

        # Notes: Could use user_id,user_name,response_url
        """
        print(request.data)
        # TODO: Improve parse command
        pprint(request.data)
        if request.data["text"] == "status":
            machine_status = list(Machine.objects.values_list("name", "status"))
            # TODO: add last brew/freshness indicator/text
            formatted_statuses = "\n".join([f"{m[0]}: {m[1]}" for m in machine_status])
            text = f"Kitchen status:\n\n{formatted_statuses or 'No machines and nothing to report 😿'}"
        else:
            text = f"Try using one of the following commands\n{' '.join(self.COMMANDS)}"

        payload = {
            "response_type": "in_channel",
            "text": text,
        }

        return Response(payload)


def _dispatch_reply(url, data):
    res = requests.post(url, json=data)
    try:
        res.raise_for_status()
    except requests.exceptions.HTTPError as err:
        print("🔥🔥🔥🔥", err)
    return res.json()


class SlackInteractionsView(APIView):
    def post(self, request):
        verify_signature(request)
        """https://api.slack.com/reference/interaction-payloads"""
        BLOCK_ID = "select_brewer_block"
        ACTION_ID = "select_brewer"

        payload = json.loads(request.data["payload"])

        brewer_action = next(filter(lambda action: action["action_id"] == ACTION_ID, payload["actions"]))
        if not brewer_action:
            return Response({"ok": False, "error": "Unsupported action_id"}, status=HTTPStatus.BAD_REQUEST)
        brewer = brewer_action["selected_user"]

        def replace_select_brewer(block):
            if block["block_id"] != BLOCK_ID:
                return block
            return {
                "block_id": BLOCK_ID,
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": f"Excellenct <@{brewer}> set as brewer. How did <@{brewer}> do?",
                    "verbatim": False,
                },
            }

        response_blocks = [replace_select_brewer(block) for block in payload["message"]["blocks"]]
        response = {
            "blocks": response_blocks,
            "replace_original": "true",
        }
        pprint(response)
        response_url = payload["response_url"]
        _dispatch_reply(response_url, data=response)

        return Response({"ok": True})


class SlackEventsView(APIView):
    SUPPORTED_EVENTS = ["reaction_added", "reaction_removed"]

    def handle_event(self, event_data):
        example_event_data = {
            "event_ts": "1629994395.027600",
            "item": {"channel": "CD42RPZL7", "ts": "1629994379.027400", "type": "message"},
            "item_user": "U02CFHANZS7",
            "reaction": "tada",
            "type": "reaction_added",
            "user": "U85U5A4P5",
        }
        event_type = event_data["type"]
        if event_type not in self.SUPPORTED_EVENTS:
            raise ValidationError("Unsupported event type")

        # TODO: Find related Brew using item.channel,item.ts tuple
        # TODO: Add/Remove reaction to/from brew

    def post(self, request):
        verify_signature(request)

        payload_type = request.data["type"]
        if payload_type == "url_verification":
            # Ref: https://api.slack.com/events/url_verification
            challenge = request.data["challenge"]
            return Response({"challenge": challenge})

        if payload_type == "event_callback":
            self.handle_event(request.data["event"])

        return Response({"ok": True})
