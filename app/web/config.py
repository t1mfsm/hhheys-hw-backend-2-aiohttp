from base64 import b64encode
import typing
from dataclasses import dataclass

import yaml
from aiohttp_session import cookie_storage

if typing.TYPE_CHECKING:
    from app.web.app import Application


@dataclass
class SessionConfig:
    key: cookie_storage.EncryptedCookieStorage


@dataclass
class AdminConfig:
    email: str
    password: str


@dataclass
class BotConfig:
    token: str = None
    group_id: int = None


@dataclass
class Config:
    admin: AdminConfig
    session: SessionConfig | None = None
    bot: BotConfig | None = None


def setup_config(app: "Application", config_path: str):
    # TODO: добавить BotConfig и (SessionConfig) по данным из config.yml
    with open(config_path, "r") as f:
        raw_config = yaml.safe_load(f)

    app.config = Config(
        admin=AdminConfig(
            email=raw_config["admin"]["email"],
            password=raw_config["admin"]["password"],
        ),
        bot=BotConfig(
            token= raw_config["bot"]["token"],
            group_id=raw_config["bot"]["group_id"],
        ),
    )
