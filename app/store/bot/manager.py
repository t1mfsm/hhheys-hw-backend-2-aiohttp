import typing

from pyexpat.errors import messages

from app.store.vk_api.dataclasses import Update, Message

if typing.TYPE_CHECKING:
    from app.web.app import Application


class BotManager:
    def __init__(self, app: "Application"):
        self.app = app

    async def handle_updates(self, updates: list[Update]):
        for update in updates:
            if update.type == "message_new":
                update_message = update.object.message
                message = Message(update_message.from_id, update_message.text)
                await self.app.store.vk_api.send_message(message)
