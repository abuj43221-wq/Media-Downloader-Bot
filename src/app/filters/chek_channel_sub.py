import asyncpg
from aiogram import Bot
from aiogram.filters import BaseFilter
from aiogram.types import Message, CallbackQuery

from src.app.database.queries.channels import ChannelDataBaseActions


class CheckSubscription(BaseFilter):

    async def __call__(self, event: Message | CallbackQuery, **data):

        pool: asyncpg.Pool = data.get("pool")
        bot: Bot = data.get("bot")

        # 🔥 SAFE CHECK
        if pool is None or bot is None:
            return False

        channel_actions = ChannelDataBaseActions(pool)
        channel_data = await channel_actions.get_all_channels()

        if not channel_data:
            return False

        for channel in channel_data:

            if channel[3] == "True":
                user_status = await bot.get_chat_member(
                    channel[0],
                    event.from_user.id
                )

                if user_status.status not in ["member", "administrator", "creator"]:
                    return True

        return False
