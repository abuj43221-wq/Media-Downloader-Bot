import asyncio
import logging
import os

import asyncpg
from aiogram import Dispatcher, Bot, Router
from aiogram.client.default import DefaultBotProperties
from aiogram.client.session.aiohttp import AiohttpSession
from aiogram.client.telegram import TelegramAPIServer
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.fsm.storage.redis import RedisStorage
from aiogram.fsm.storage.base import DefaultKeyBuilder
from aiogram_dialog import setup_dialogs

from logs.loggger_conf import setup_logging
from src.app.common.bot_commands import bot_commands
from src.app.common.database_backup import daily_database_sender
from src.app.common.db_url import construct_postgresql_url
from src.app.common.requirements_updater import requirements_updater
from src.app.core.config import Settings
from src.app.database.tables import create_database_tables
from src.app.dialogs import register_all_dialogs
from src.app.handlers import register_all_router
from src.app.middleware import register_middleware

logger = logging.getLogger(__name__)


async def main():
    settings = Settings()
    dsn = construct_postgresql_url(settings)

    pool = None

    # 🔥 SAFE DB CONNECTION (NO CRASH)
    try:
        pool = await asyncpg.create_pool(dsn, ssl=True)

        async with pool.acquire() as conn:
            await create_database_tables(conn)

        print("✅ Database connected")

    except Exception as e:
        pool = None
        logger.error(f"❌ DB error: {e}")
        print("⚠️ Bot running without database")

    # 🔥 STORAGE (SAFE)
    if settings.bot_user_redis:
        try:
            key_builder = DefaultKeyBuilder(with_destiny=True)
            storage = RedisStorage.from_url(
                f"redis://{settings.redis_host}:6379/{settings.redis_db_name}",
                key_builder=key_builder
            )
        except Exception as e:
            logger.error(f"Redis error: {e}")
            storage = MemoryStorage()
    else:
        storage = MemoryStorage()

    dp = Dispatcher(storage=storage)

    dialogs_router = Router()
    other_router = Router()

    register_all_dialogs(dialogs_router)

    # middleware (pool None safe pass)
    register_middleware(dp, settings, pool)

    register_all_router(dp, settings)

    dp.include_router(dialogs_router)
    dp.include_router(other_router)

    setup_dialogs(dp)

    session = AiohttpSession(
        api=TelegramAPIServer.from_base(settings.tg_api_server_url)
    )

    bot = Bot(
        token=settings.bot_token,
        session=session,
        default=DefaultBotProperties(parse_mode="HTML")
    )

    # background tasks (safe even without DB)
    asyncio.create_task(requirements_updater())

    if pool:
        asyncio.create_task(
            daily_database_sender(bot, settings.admins_ids, pool)
        )

    await bot_commands(bot, settings)

    # 🚀 BOT ALWAYS RUNS (IMPORTANT FIX)
    await dp.start_polling(bot)


if __name__ == "__main__":
    try:
        setup_logging("logs/logger.yml")

        os.makedirs("media/videos", exist_ok=True)
        os.makedirs("media/audios", exist_ok=True)
        os.makedirs("media/photos", exist_ok=True)

        asyncio.run(main())

    except Exception as e:
        logger.exception(e)
