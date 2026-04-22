import re
import asyncio

import asyncpg
from aiogram import Router, F
from aiogram.filters import CommandStart, CommandObject, Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.enums import ChatAction


from src.app.database.queries.referals import ReferalDataBaseActions
from src.app.database.queries.users import UserDataBaseActions
from src.app.utils.i18n import get_translator

start_router = Router()


# 🔥 START COMMAND
@start_router.message(CommandStart())
async def command_start(message: Message):

    await message.bot.send_chat_action(message.chat.id, ChatAction.TYPING)
    await asyncio.sleep(1)

    text = f"""
👋🏻 Hello {message.from_user.first_name or message.from_user.username}

📥 I can help you download videos and images from:

▶️ YouTube  
📸 Instagram  
🎵 TikTok  
📌 Pinterest  
👻 Snapchat  
🔥 Likee  
🌐 VK  
📘 Facebook  
🧵 Threads  
🎧 Music  

━━━━━━━━━━━━━━━  
📎 Send any link to download instantly  

👥 Works in groups too 👇
"""

    buttons = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="➕ Add to Group",
                    url=f"https://t.me/{(await message.bot.get_me()).username}?startgroup=true"
                )
            ],
            [
                InlineKeyboardButton(text="ℹ️ Help", callback_data="help"),
                InlineKeyboardButton(text="📘 About", callback_data="about")
            ],
            [
                InlineKeyboardButton(text="📢 Support", url="https://t.me/anujeditbyak")
            ]
        ]
    )

    await message.answer_photo(
        photo="https://h.uguu.se/vCWUTJSx.jpg",
        caption=text,
        reply_markup=buttons
    )


# 🔥 HELP COMMAND
@start_router.message(Command("help"))
async def help_command(message: Message):
    await message.answer(
        "📌 *How to use the bot*\n\n"
        "1. Copy any video/image link\n"
        "2. Send it here\n"
        "3. Get your download instantly 🚀\n\n"
        "Supported:\n"
        "▶️ YouTube\n📸 Instagram\n🎵 TikTok\n📘 Facebook",
        parse_mode="Markdown"
    )


# 🔥 ABOUT COMMAND
@start_router.message(Command("about"))
async def about_command(message: Message):
    await message.answer(
        "🤖 *About This Bot*\n\n"
        "This bot helps you download media from multiple platforms.\n\n"
        "⚡ Fast\n🎯 Easy to use\n💯 Free\n\n"
        "👨‍💻 Developed for automation lovers ❤️",
        parse_mode="Markdown"
    )


# 🔘 HELP BUTTON
@start_router.callback_query(F.data == "help")
async def help_callback(callback):
    await callback.message.answer(
        "📌 Send any video or image link.\n\nExample:\nhttps://youtube.com/..."
    )
    await callback.answer()


# 🔘 ABOUT BUTTON
@start_router.callback_query(F.data == "about")
async def about_callback(callback):
    await callback.message.answer(
        "🤖 Media Downloader Bot\n\nFast & powerful downloader 🚀"
    )
    await callback.answer()
