import os
from dotenv import load_dotenv
from swiftclient import Connection
load_dotenv()


class SwiftConnection():
    _instance = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self, authurl, user, key, auth_version) -> None:
        self.connection = Connection(
            authurl=authurl,
            user=user,
            key=key,
            auth_version=auth_version,
            retries=3
        )

    def close(self):
        self.connection.close()

    async def put(
        self,
        obj: str,
        contents,
    ):
        return self.connection.put_object(
            container='documents',
            obj=obj,
            contents=contents
        )

    async def read():
        pass


def get_swift_connection():
    return SwiftConnection(
        authurl=os.getenv('SWIFT_AUTH_URL'),
        user=os.getenv('SWIFT_ACCOUNT'),
        key=os.getenv('SWIFT_KEY'),
        auth_version=os.getenv('SWIFT_AUTH_VERSION')
    )