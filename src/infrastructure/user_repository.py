from http.cookiejar import Cookie as HttpCookie, CookieJar
from pydantic.main import BaseModel
from typing import Optional
from httpx import AsyncClient
import requests # type: ignore
import datetime

_client = AsyncClient()


class CredentialsError(Exception):
    pass


class Cookie(BaseModel):
    value: str = ""
    expires: Optional[int] = None
    path: str = "/"
    domain: Optional[str] = None


class UserRepository:

    user_cookies: dict[str, str] = {
        "marc12info@gmail.com": "231784%7C1662297339%7C6382a5b012afdf595dec0bbd49f6e13a",
        "glezgutierrez95@gmail.com": "121104%7C1662979653%7C75ad1e2b789c4ced9460f3e214516cf7"
    }

    async def login(self, mail: str, pw: str) -> dict[str, Cookie]:

        # TODO: Make this async
        # Login to alphalink
        session = requests.Session()
        _ = session.post(
            "https://alphalinkcrossfit.aimharder.com/login",
            data={"login": "Log in", "mail": mail, "pw": pw},
        )

        # Alphalink API adds amhrdauth cookie when logging in
        if "amhrdrauth" not in session.cookies.get_dict():
            raise CredentialsError("Login Error")

        # Store cookie
        self.user_cookies[mail] = session.cookies.get("amhrdrauth")

        # Return cookie domain object
        return {
            cookie.name: Cookie(
                value=cookie.value,
                expires=cookie.expires,
                path=cookie.path,
                domain=cookie.domain,
            )
            for cookie in list(session.cookies)
        }

    async def is_cookie_valid(self, amhrdauth: str) -> bool:
        # Try to access settings page, if redirected to login. The key is invalid

        response = await _client.get(
            f"https://aimharder.com/settings",
            cookies=self.amhrdrauth_string_to_cookie(amhrdauth=amhrdauth),
            follow_redirects=True,
        )
        if response.url == "https://aimharder.com/settings":
            return True

        return False

    async def set_auth_cookie(self, mail: str, amhrdauth: str) -> None:

        if not await self.is_cookie_valid(amhrdauth=amhrdauth):
            raise Exception("Invalid login credentials")

        self.user_cookies[mail] = amhrdauth

    def amhrdrauth_string_to_cookie(self, amhrdauth: str) -> CookieJar:
        cj = CookieJar()
        c = HttpCookie(
            version=0,
            name="amhrdrauth",
            value=amhrdauth,
            port=None,
            port_specified=False,
            domain=".aimharder.com",
            domain_specified=True,
            domain_initial_dot=False,
            path="/",
            path_specified=True,
            secure=False,
            expires=int(
                (datetime.datetime.now() + datetime.timedelta(days=7)).timestamp()
            ),
            discard=False,
            comment=None,
            comment_url=None,
            rest={"httponly": "None"},
            rfc2109=False,
        )
        cj.set_cookie(c)
        return cj

    async def get_cookies(self, mail: str) -> Optional[CookieJar]:

        auth_cookie = self.user_cookies.get(mail)

        if auth_cookie:
            return self.amhrdrauth_string_to_cookie(auth_cookie)

        return None

    async def clean_cookies(self) -> None:
        self.user_cookies = {}
