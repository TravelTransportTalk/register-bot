from dataclasses import dataclass
from dataclasses_json import dataclass_json


@dataclass_json
@dataclass
class User:
    nick: str
    fullName: str
    description: str
    tgUsername: str
    tgId: int


@dataclass_json
@dataclass
class AuthUserRequest:
    tgId: int

@dataclass_json
@dataclass
class UserControllerResp:
    message: str
    user: User