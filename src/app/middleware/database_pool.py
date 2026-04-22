from typing import Callable, Dict, Any, Awaitable, Optional

import asyncpg
from aiogram import BaseMiddleware
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

        # 🔥 SAFE MODE: if DB not available, skip injection
        if self.pool is None:
            return await handler(event, data)

        # inject pool into handlers
        data["pool"] = self.pool

        return await handler(event, data)
