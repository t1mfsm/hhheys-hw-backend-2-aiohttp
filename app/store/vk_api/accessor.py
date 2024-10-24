import typing
from random import random, randint
from urllib.parse import urlencode, urljoin

import aiohttp
from aiohttp.client import ClientSession

from app.base.base_accessor import BaseAccessor
from app.store import Store
from app.store.vk_api.dataclasses import Message
from app.store.vk_api.poller import Poller

if typing.TYPE_CHECKING:
    from app.web.app import Application

API_VERSION = "5.131"


class VkApiAccessor(BaseAccessor):
    def __init__(self, app: "Application", *args, **kwargs):
        super().__init__(app, *args, **kwargs)
        self.session: ClientSession | None = None
        self.key: str | None = None
        self.server: str | None = None
        self.poller: Poller | None = None
        self.ts: int | None = None

    async def connect(self, app: "Application"):
        self.session = aiohttp.ClientSession(
                connector=aiohttp.TCPConnector(ssl=False)
        )
        raw_data = await self._get_long_poll_service()
        self.app.store.vk_api.server = raw_data.get("response").get("server")
        self.key = raw_data.get("response").get("key")
        self.ts = raw_data.get("response").get("ts")
        self.poller = Poller(self.app.store)
        await self.poller.start()

        #  получить данные о long poll сервере с помощью метода groups.getLongPollServer
        #  вызвать метод start у Poller
        # raise NotImplementedError

    async def disconnect(self, app: "Application"):
        await self.poller.stop()
        await self.session.close()
        # TODO: закрыть сессию и завершить поллер

    @staticmethod
    def _build_query(host: str, method: str, params: dict) -> str:
        params.setdefault("v", API_VERSION)
        return f"{urljoin(host, method)}?{urlencode(params)}"

    async def _get_long_poll_service(self):
        async with self.session.get(
            f"https://api.vk.ru/method/groups.getLongPollServer?access_token={self.app.config.bot.token}&group_id={self.app.config.bot.group_id}&v=5.199") as response:
            return await response.json()

    async def poll(self):
        raise NotImplementedError

    async def send_message(self, message: Message) -> None:
        await self.session.get(
                f"https://api.vk.ru/method/messages.send?access_token={self.app.config.bot.token}&user_id={message.user_id}&message=Какое-то сообщение&random_id={int(randint(1,999999999))}&v=5.199")
