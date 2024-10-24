from aiohttp_session import get_session
from aiohttp.web_exceptions import HTTPUnauthorized, HTTPForbidden


class AuthRequiredMixin:
    async def check_auth(self, request):
        session = await get_session(request)
        data = session.get("manager")
        if not data:
            raise HTTPUnauthorized
        else:
            return data

