# pip dependency
import typing
from starlette.authentication import AuthenticationBackend, SimpleUser, AuthCredentials
from starlette.requests import HTTPConnection
from jose import jwt
# local dependency
from config.setting import settings
from config import security


class CustomAuthBackend(AuthenticationBackend):

    async def authenticate(self, conn: HTTPConnection) -> \
            typing.Optional[typing.Tuple["AuthCredentials", "CustomSimpleUser"]]:
        if "Authorization" not in conn.headers:
            return
        auth = conn.headers["authorization"]
        scheme, credential =auth.split()
        if scheme.lower() != 'bearer':
            return
        else:
            payload = jwt.decode(
                        credential, settings.SECRET_KEY, algorithms=[security.ALGORITHM]
            )

            if payload['is_superuser']:
                return AuthCredentials(["authenticated", "admin"]), \
                       CustomSimpleUser(id=payload['sub'], is_superuser=payload['is_superuser'])
            else:
                return AuthCredentials(["authenticated"]), \
                       CustomSimpleUser(id=payload["sub"], is_superuser=payload["is_superuser"])


class CustomSimpleUser(SimpleUser):
    def __init__(self, id: int, is_superuser: bool) -> None:
        self.id = id
        self.is_superuser = is_superuser


    @property
    def identity(self) -> int:
        return self.id


custom_backend = CustomAuthBackend()
