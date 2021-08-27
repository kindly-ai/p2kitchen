import json
import logging

import requests
import urllib.parse
from django.conf import settings
from rest_framework.exceptions import ValidationError
from slack_sdk.signature import SignatureVerifier

logger = logging.getLogger(__name__)

SLACK_API_URL_BASE = "https://slack.com/api/"


def _dispatch(method, **data):
    headers = {
        "Authorization": f"Bearer {settings.SLACK_API_TOKEN}",
        "Content-type": "application/json; charset=utf-8",
    }

    url = f"{SLACK_API_URL_BASE}{method}"
    logger.debug("Sending request to slack with data: %s", json.dumps(data))

    response = requests.post(url, headers=headers, json=data)
    content = json.loads(response.content.decode())

    error = content.get("error")
    if error:
        logger.error(
            "Method %s, got response: ok=%s, %s",
            method,
            str(content["ok"]),
            "error=" + error,
        )
    else:
        logger.debug("Method %s, got response: ok=%s", method, str(content["ok"]))
    return content


def _upload(method, f, channels=None, **data):
    params = {
        "token": settings.SLACK_API_TOKEN,
    }

    if channels:
        params["channels"] = ",".join(channels)

    for k, v in data.items():
        if k is not None and v is not None:
            params[k] = v

    params = urllib.parse.urlencode(params)

    url = f"{SLACK_API_URL_BASE}{method}?{params}"
    logger.debug("Uploading file to slack.")

    response = requests.post(url, files={"file": ("current.jpg", f)})
    content = json.loads(response.content.decode())

    error = content.get("error")
    if error:
        logger.error(
            "Method %s, Got response: ok=%s, %s",
            method,
            str(content["ok"]),
            "error=" + error,
        )
    else:
        logger.debug("Method %s, Got response: ok=%s", method, str(content["ok"]))
    return content


def conversations_list():
    return _dispatch("conversations.list")


def channels_info(channel):
    return _dispatch("channels.info", channel=channel)


def channels_join(channel):
    return _dispatch("channels.join", channel=channel)


def chat_post_message(channel, blocks=None, text=None, attachments=None):
    data = {
        "channel": channel,
    }

    if text is not None:
        data["text"] = text

    if attachments is not None:
        data["attachments"] = attachments

    if blocks is not None:
        data["blocks"] = blocks

    return _dispatch("chat.postMessage", **data)


def chat_update(channel, timestamp, text):
    data = {
        "channel": channel,
        "ts": timestamp,
        "text": text,
    }

    return _dispatch("chat.update", **data)


def chat_delete(channel, timestamp):
    data = {
        "channel": channel,
        "ts": timestamp,
    }

    return _dispatch("chat.delete", **data)


def files_upload(f, filename=None, filetype=None, title=None, initial_comment=None, channels=None):
    return _upload(
        "files.upload",
        f,
        filename=filename,
        filetype=filetype,
        title=title,
        initial_comment=initial_comment,
        channels=channels,
    )


def verify_signature(request):
    """https://api.slack.com/authentication/verifying-requests-from-slack"""
    verifier = SignatureVerifier(settings.SLACK_SIGNING_SECRET)
    if not verifier.is_valid_request(request.body, request.headers):
        raise ValidationError("Invalid slack signature")
