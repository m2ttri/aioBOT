import asyncio

from aiogram import Bot, Dispatcher

from config import BOT_TOKEN
from handlers import router


ALLOWED_UPDATES = ['message']

bot = Bot(token=f'{BOT_TOKEN}')
dp = Dispatcher()

dp.include_router(router)


async def main():
    while True:
        try:
            await bot.delete_webhook(drop_pending_updates=True)
            await dp.start_polling(bot, allowed_updates=ALLOWED_UPDATES)
        except Exception as e:
            print(f'ERROR: {e}')
            await asyncio.sleep(5)

asyncio.run(main())
