import asyncio
import logging

from aiogram import Bot, Dispatcher

from config import settings
from handlers import callbacks, group_messages, private


async def main() -> None:
    """
    Точка входа в бота.

    Здесь:
    1. Настраиваем логирование.
    2. Создаём Bot.
    3. Создаём Dispatcher.
    4. Подключаем роутеры с обработчиками.
    5. Запускаем long polling.
    """

    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
    )

    bot = Bot(token=settings.bot_token)
    dp = Dispatcher()

    # Подключаем обработчики.
    # private — /start в личке.
    # callbacks — кнопки Да/Нет.
    # group_messages — чтение вакансий из группы.
    dp.include_router(private.router)
    dp.include_router(callbacks.router)
    dp.include_router(group_messages.router)

    try:
        logging.info("Бот запущен через long polling.")
        await dp.start_polling(
            bot,
            allowed_updates=dp.resolve_used_update_types(),
        )
    finally:
        await bot.session.close()


if __name__ == "__main__":
    asyncio.run(main())
