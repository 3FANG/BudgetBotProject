from dataclasses import dataclass
from typing import Union, List

from aiogram.filters import BaseFilter
from aiogram.types import Message



@dataclass
class ChatTypeFilter(BaseFilter):
    chat_type: Union[str, list]

    async def __call__(self, message: Message) -> bool:
        if isinstance(self.chat_type, str):
            return message.chat.type == self.chat_type
        else:
            return message.chat.type in self.chat_type


@dataclass
class AdminFilter(BaseFilter):
    admin_ids: list[int]

    async def __call__(self, message: Message) -> bool:
        return message.from_user.id in self.admin_ids
