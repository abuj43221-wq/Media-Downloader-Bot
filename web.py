from aiohttp import web
import asyncio
from src.app.main import main

async def handle(request):
    return web.Response(text="Bot is running")

async def start_web():
    app = web.Application()
    app.router.add_get("/", handle)

    runner = web.AppRunner(app)
    await runner.setup()

    site = web.TCPSite(runner, "0.0.0.0", 10000)
    await site.start()

async def main_wrapper():
    await asyncio.gather(
        main(),
        start_web()
    )

if __name__ == "__main__":
    asyncio.run(main_wrapper())
