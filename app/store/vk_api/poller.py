import asyncio
from asyncio import Task

from app.store import Store
from app.store.vk_api.dataclasses import Update, UpdateMessage, UpdateObject


class Poller:
    def __init__(self, store: Store) -> None:
        self.store = store
        self.is_running = False
        self.poll_task: Task | None = None

    async def start(self) -> None:
        self.poll_task = asyncio.create_task(self.poll())
        self.is_running = True

    async def stop(self) -> None:
        self.poll_task.cancel()
        self.is_running = False

    async def poll(self) -> None:
        async with self.store.vk_api.session.get(f"{self.store.vk_api.server}?act=a_check&key={self.store.vk_api.key}&ts={self.store.vk_api.ts}&wait=5&mode=2&version=2") as response:
            data = await response.json()
            self.store.vk_api.ts = data.get("ts")
            if len(data.get("updates")) != 0:
                updates = []
                for i in data.get("updates"):
                    if i.get("type") == "message_new":
                        message_data = i.get("object").get("message")
                        message = UpdateMessage(message_data.get("from_id"), message_data.get("text"), message_data.get("id"))
                        updates.append(Update("message_new", UpdateObject(message)))
                await self.store.bots_manager.handle_updates(updates)

        if self.is_running:
            await self.poll()
