from http.cookiejar import Cookie as HttpCookie, CookieJar
from typing import Optional
from httpx import AsyncClient
import requests # type: ignore
import datetime
from beanie import Document
from pydantic import Field
from src.entities.user import User

from src.output_ports.user_port import Cookie, CredentialsError, UserPort

_client = AsyncClient()


class Users(Document):
    email: str
    token: str
    created_at: datetime.datetime = Field(default_factory=datetime.datetime.now)
    updated_at: datetime.datetime = Field(default_factory=datetime.datetime.now)


def db_to_domain(user: Users) -> User:
    return User(
        email=user.email,
        token=user.token,
        created_at=user.created_at,
        updated_at=user.updated_at
    )


def domain_to_db(user: User) -> Users:
    return Users(
        email=user.email,
        token=user.token,
        created_at=user.created_at,
        updated_at=user.updated_at
    )

    
class UserMongoRepository(UserPort):


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
        user = Users(
            email=mail,
            token=session.cookies.get("amhrdrauth")
        )

        await Users \
            .find_one(Users.email == user.email) \
            .upsert({"$set": {"token": user.token, "updated_at": user.updated_at}}, on_insert=user)

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

        user = Users(
            email=mail,
            token=amhrdauth
        )

        await Users \
            .find_one(Users.email == user.email) \
            .upsert({"$set": {"token": user.token}}, on_insert=user)

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

        user = await Users.find_one(Users.email == mail)

        if user:
            return self.amhrdrauth_string_to_cookie(user.token)

        return None

    async def clean_cookies(self) -> None:
        pass

    async def get_all(self) -> list[User]:
        return [db_to_domain(user) async for user in Users.find()]