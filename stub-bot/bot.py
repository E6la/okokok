import asyncio
import logging
import os

from aiogram import Bot, Dispatcher
from aiogram.filters import CommandStart
from aiogram.types import Message

dp = Dispatcher()


@dp.message(CommandStart())
async def start(message: Message) -> None:
    """Ответ на /start."""

    await message.answer(
        "Привет! Я бот-заглушка и работаю на серверах GitHub.\n"
        "Напиши мне что-нибудь — я отвечу."
    )


@dp.message()
async def echo(message: Message) -> None:
    """Ответ на любое другое сообщение."""

    if message.text:
        await message.answer(f"Ты написал: {message.text}")
    else:
        await message.answer("Получил сообщение, но умею отвечать только на текст.")


async def main() -> None:
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
    )

    token = os.getenv("BOT_TOKEN")
    if not token:
        raise RuntimeError("Не задан BOT_TOKEN (добавь его в секреты репозитория)")

    bot = Bot(token=token)
    try:
        logging.info("Бот-заглушка запущен через long polling.")
        await dp.start_polling(bot)
    finally:
        await bot.session.close()


if __name__ == "__main__":
    asyncio.run(main())
