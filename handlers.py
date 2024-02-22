from aiogram import Router, types
from aiogram.filters import CommandStart, Command
from utils import utils


router = Router()


@router.message(CommandStart())
async def start_cmd(message: types.Message):
    """Приветствие пользователя, команда /start"""

    username = await utils.get_user_name(message)
    await message.answer(f'Hello <b>{username}</b> 🐱', parse_mode='html')


@router.message(Command('w'))
async def weather_cmd(message: types.Message):
    """Получить погоду в указанном городе, команда /w *город*"""

    weather = await utils.get_weather(message)
    await message.answer(weather)


@router.message(Command('v', 'p'))
async def random_content_cmd(message: types.Message):
    """Получить случайное изображение или видео PEXELS_API,
    команда /p или /v *категория* *количество*"""

    total_results = await utils.get_total_results(message.text)

    if total_results == 0:
        await message.answer(f'Total results: {total_results}')

    else:
        await message.answer('Uploading...')

        counter = 1

        async for item, category in utils.get_random_content(message.text):
            try:
                if category == 'video':
                    await message.answer_video(
                        video=types.BufferedInputFile(
                            file=item,
                            filename='item.mp4'
                        ),
                        caption=f'#{counter}'
                    )
                else:
                    await message.answer_photo(
                        photo=types.BufferedInputFile(
                            file=item,
                            filename='item.jpg'
                        ),
                        caption=f'#{counter}'
                    )
            except Exception as e:
                await message.answer(f'#{counter} Telegram error!')
                print(e)

            counter += 1

        await message.answer('Done!')
