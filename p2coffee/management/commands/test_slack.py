import json
import time

from django.core.management import BaseCommand, CommandError
from p2coffee import slack


def _print_as_json(data):
    print(json.dumps(data, indent=2))


class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument("channel_name", nargs="?", default="kitchen-dev")

    def handle(self, channel_name, *args, **options):
        channels = slack.conversations_list().get("channels", [])
        channel_data = next(filter(lambda channel: channel["name"] == channel_name, channels), None)
        if not channel_data:
            raise CommandError(f"Couldn't find the channel {channel_name} :(")
        channel_id = channel_data["id"]
        print("🔥", channel_id)
        BLOCK_ID = "select_brewer_block"
        ACTION_ID = "select_brewer"
        blocks = [
            {
                "type": "section",
                "block_id": "brew_block",
                "text": {
                    "type": "mrkdwn",
                    "text": "Brew 11233 ready. Grutenberg started brewing at 10:09:30 and finished at 10:13:53!",
                },
            },
            {
                "type": "section",
                "block_id": BLOCK_ID,
                "text": {
                    "type": "mrkdwn",
                    "text": "Pick the user who brewed this batch from the dropdown list",
                },
                "accessory": {
                    "action_id": ACTION_ID,
                    "type": "users_select",
                    "placeholder": {"type": "plain_text", "text": "Select a brewer"},
                },
            },
        ]
        post_response = slack.chat_post_message(channel_id, blocks=blocks)
        _print_as_json(post_response)
        msg_ts = post_response["ts"]

        # time.sleep(15)
        # update_response = slack.chat_update(
        #     channel_id, msg_ts, "Ignorer meg, men..." + text
        # )
        # print_as_json(update_response)

        # Delete message
        # time.sleep(7)
        # delete_response = slack.chat_delete(channel_id, msg_ts)
        # _print_as_json(delete_response)
