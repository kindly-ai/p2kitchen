import json
import logging

import requests
import urllib.parse
from django.conf import settings
from rest_framework.exceptions import ValidationError
from slack_sdk.signature import SignatureVerifier

logger = logging.getLogger(__name__)

SLACK_API_URL_BASE = "https://slack.com/api/"


def _dispatch(method, **kwargs):
    headers = {
        "Authorization": f"Bearer {settings.SLACK_API_TOKEN}",
    }
    if "json" in kwargs:
        headers["Content-type"] = "application/json; charset=utf-8"

    url = f"{SLACK_API_URL_BASE}{method}"
    data = kwargs.get("json", {}) if "json" in kwargs else kwargs.get("data", {})
    logger.debug("Sending request to slack with data: %s", json.dumps(data, indent=2, ensure_ascii=False))

    response = requests.post(url, headers=headers, **kwargs)
    content = response.json()

    error = content.get("error")
    if error:
        logger.error(f"Method {method}, got response: ok={content['ok']}, {error=}")
    else:
        logger.debug(f"Method {method}, got response: ok={content['ok']}")
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

    url = f"{SLACK_API_URL_BASE}{method}"
    logger.debug("Uploading file to slack.")

    response = requests.post(url, params=params, files={"file": ("current.jpg", f)})
    content = json.loads(response.content.decode())

    error = content.get("error")
    if error:
        logger.error(f"Method {method}, got response: ok={content['ok']}, {error=}")
    else:
        logger.debug(f"Method {method}, got response: ok={content['ok']}")
    return content


def conversations_list():
    return _dispatch("conversations.list")


def channels_info(channel):
    return _dispatch("channels.info", json={"channel": channel})


def channels_join(channel):
    return _dispatch("channels.join", json={"channel": channel})


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

    return _dispatch("chat.postMessage", json=data)


def chat_update(channel, timestamp, text=None, blocks=None):
    data = {
        "channel": channel,
        "ts": timestamp,
    }
    if text:
        data["text"] = text

    if blocks:
        data["blocks"] = blocks

    return _dispatch("chat.update", json=data)


def chat_delete(channel, timestamp):
    data = {
        "channel": channel,
        "ts": timestamp,
    }

    return _dispatch("chat.delete", json=data)


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


def users_profile_get(user):
    """https://api.slack.com/methods/users.profile.get"""
    data = {"user": user}
    return _dispatch("users.profile.get", data=data)


def verify_signature(request):
    """https://api.slack.com/authentication/verifying-requests-from-slack"""
    if not settings.SLACK_SIGNING_SECRET:
        raise ValueError("SLACK_SIGNING_SECRET not set in")
    verifier = SignatureVerifier(settings.SLACK_SIGNING_SECRET)
    if not verifier.is_valid_request(request.body, request.headers):
        raise ValidationError("Invalid slack signature")
