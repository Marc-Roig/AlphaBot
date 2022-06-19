from typing import Optional, Protocol
from http.cookiejar import Cookie as HttpCookie, CookieJar
from pydantic import BaseModel

class CredentialsError(Exception):
    pass


class Cookie(BaseModel):
    value: str = ""
    expires: Optional[int] = None
    path: str = "/"
    domain: Optional[str] = None


class UserPort(Protocol):

    async def login(self, mail: str, pw: str) -> dict[str, Cookie]:
        pass

    async def is_cookie_valid(self, amhrdauth: str) -> bool:
        pass

    async def set_auth_cookie(self, mail: str, amhrdauth: str) -> None:
        pass

    async def get_cookies(self, mail: str) -> Optional[CookieJar]:
        pass

    async def clean_cookies(self) -> None:
        pass