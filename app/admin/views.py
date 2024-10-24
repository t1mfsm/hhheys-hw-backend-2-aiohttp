from aiohttp import request, ClientSession
from aiohttp_session import get_session, session_middleware, cookie_storage, new_session, AbstractStorage

from app.web.app import View
from app.web.mixins import AuthRequiredMixin
from app.web.utils import json_response

from aiohttp.web_exceptions import HTTPForbidden


class AdminLoginView(View):
    async def post(self):
        data = await self.request.json()
        if await self.request.app.store.admins.validate_admin(data["email"], data["password"]):
            admin = await self.request.app.store.admins.get_by_email(data["email"])
            admin_data = {
                "id":admin.id,
                "email":admin.email
            }
            session = await new_session(request=self.request)
            session['manager'] = admin_data

            return json_response(data=admin_data)
        else:
            raise HTTPForbidden


class AdminCurrentView(View, AuthRequiredMixin):
    async def get(self):
        admin_data = await self.check_auth(self.request)
        return json_response(data=admin_data)
