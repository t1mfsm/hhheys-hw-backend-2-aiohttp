import typing

from marshmallow.fields import Boolean

from app.admin.models import Admin
from app.base.base_accessor import BaseAccessor
from app.web.config import AdminConfig, Config
from tests.conftest import config

if typing.TYPE_CHECKING:
    from app.web.app import Application


class AdminAccessor(BaseAccessor):
    async def connect(self, app: "Application") -> None:
        self.app = app
        await self.create_admin(self.app.config.admin.email, self.app.config.admin.password)

    async def get_by_email(self, email: str) -> Admin | None:
        for admin in self.app.database.admins:
            if admin.email == email:
                return admin
        return None

    async def create_admin(self, email: str, password: str) -> Admin:
        admin = Admin(self.app.database.next_admin_id, email, hash(password))
        self.app.database.admins.append(admin)
        return admin

    async def validate_admin(self, email: str, password: str) -> bool:
        for admin in self.app.database.admins:
            if admin.email == email and admin.password == hash(password):
                return True
        return False
