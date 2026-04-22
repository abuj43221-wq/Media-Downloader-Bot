from typing import Callable, Dict, Any, Awaitable, Optional

import asyncpg
from aiogram import BaseMiddleware, Bot
from aiogram.types import TelegramObject, CallbackQuery, Message


class DatabaseMiddleware(BaseMiddleware):
    def __init__(self, pool: Optional[asyncpg.Pool]):
        self.pool = pool

    async def __call__(
        self,
        handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
        event: Message | CallbackQuery,
        data: Dict[str, Any]
    ) -> Any:

        # 🔥 ALWAYS inject bot (important)
        data["bot"] = data.get("bot")

        # 🔥 SAFE DB handling
        if self.pool is not None:
            data["pool"] = self.pool
        else:
            data["pool"] = None  # explicit safe state

        return await handler(event, data)
