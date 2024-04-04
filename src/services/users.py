import json
from typing import Generic, TypeVar, Dict

from src.data_init import logger
from src.models.user import *


import requests
import dataclasses


class UserService:

    def __init__(self, api_url: str) -> None:
        self.api_url = api_url

    async def create_user(self, data: User):
        url = f'{self.api_url}/register'
        response = requests.post(url, json=dataclasses.asdict(data))
        if response.ok and response.text != "":
            return True
        else:
            logger.info(response.text)
            return None

    async def auth(self, tg_id: int) -> User | None:
        url = f'{self.api_url}/auth'
        response = requests.post(url, json=dataclasses.asdict(AuthUserRequest(tg_id)))
        if response.ok and response.text != "":
            return UserControllerResp.from_json(response.text).user
        else:
            logger.info(response.text)
            return None

    async def change(self, request: ChangeUserRequest) :
        url = f'{self.api_url}/change'
        response = requests.post(url, json=dataclasses.asdict(request))
        if response.ok and response.text != "":
            return True
        else:
            logger.info(response.text)
            return None
