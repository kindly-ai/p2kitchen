from typing import TYPE_CHECKING

from django.conf import settings
from django.utils import timezone

from p2coffee.utils import format_local_timestamp

if TYPE_CHECKING:
    from p2coffee.models import Brew

SELECT_BREWER_BLOCK_ID = "select_brewer_block"
SELECT_BREWER_ACTION_PREFIX = "select_brewer"


def _create_progress_bar(percent: int):
    assert 0 <= percent <= 100
    symbol_filled = "☕"
    symbol_unfilled = "_"
    max_width = 32

    normalized = int((percent / 100) * max_width)

    filled_chars = "".join([symbol_filled] * normalized)
    unfilled_chars = "".join([symbol_unfilled] * (max_width - normalized))

    return f"`[{filled_chars}{unfilled_chars}] {percent}%`"


def _format_brew_block(status_text: str):
    return {
        "type": "section",
        "block_id": "brew_block",
        "text": {"type": "mrkdwn", "text": status_text},
    }


def _format_selected_brewer_block(brew: "Brew"):
    if not brew.brewer:
        return {
            "type": "section",
            "block_id": SELECT_BREWER_BLOCK_ID,
            "text": {
                "type": "mrkdwn",
                "text": "Select the user who's brewing this batch",
            },
            "accessory": {
                "action_id": f"{SELECT_BREWER_ACTION_PREFIX}:{brew.pk}",
                "type": "users_select",
                "placeholder": {"type": "plain_text", "text": "Select a brewer"},
            },
        }
    return {
        "type": "section",
        "block_id": SELECT_BREWER_BLOCK_ID,
        "text": {
            "type": "mrkdwn",
            "text": f"<@{brew.brewer.user_id}> brewed this batch. How did they do?",
            "verbatim": False,
        },
    }


def brew_started_message(brew: "Brew"):
    start_time = format_local_timestamp(brew.created, "%H:%M:%S")
    status_text = f"{brew.machine.name} started brewing at {start_time}"
    return {"blocks": [_format_brew_block(status_text)]}


def brew_update_message(brew: "Brew"):
    start_time = format_local_timestamp(brew.created, "%H:%M:%S")
    status_text = f"{brew.machine.name} started brewing at {start_time}"

    duration = (timezone.now() - brew.created).seconds
    avg_brewtime = settings.BREWTIME_AVG_SECONDS

    if duration > avg_brewtime:
        progress_msg = _create_progress_bar(100)
        status_text = f"{status_text}...looks like I'm a bit slow today...\n{progress_msg}"
    else:
        progress = int(100 * (duration / avg_brewtime))
        status_text = f"{status_text}\n{_create_progress_bar(progress)}"

    blocks = [_format_brew_block(status_text), _format_selected_brewer_block(brew)]
    return {"blocks": blocks}


def brew_finished_message(brew: "Brew"):
    start_time = format_local_timestamp(brew.started_event.created, "%H:%M:%S")
    end_time = format_local_timestamp(brew.finished_event.created, "%H:%M:%S")
    status_text = (
        f"Brew {brew.pk} ready. {brew.machine.name} started brewing at {start_time} and finished at {end_time}"
    )
    blocks = [_format_brew_block(status_text), _format_selected_brewer_block(brew)]
    return {"blocks": blocks}
