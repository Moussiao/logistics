from typing import TYPE_CHECKING

import pytest

from src.apps.tg_bots.services import TgSendMessage

if TYPE_CHECKING:
    from pytest_mock import MockerFixture, MockType

    from src.apps.tg_bots.models import TgChat


pytestmark = [pytest.mark.django_db]


@pytest.fixture
def mock_send_message(mocker: "MockerFixture") -> "MockType":
    return mocker.patch("telegram.ext.ExtBot.send_message")


@pytest.mark.asyncio
async def test_send_message(tg_chat: "TgChat", mock_send_message: "MockType") -> None:
    await TgSendMessage(text="text", chat=tg_chat)()

    mock_send_message.assert_called_once_with(chat_id=tg_chat.external_id * -1, text="text")
