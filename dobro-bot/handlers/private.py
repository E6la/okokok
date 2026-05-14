from aiogram import Router
from aiogram.filters import CommandStart
from aiogram.types import Message

from config import settings

router = Router(name=__name__)


@router.message(CommandStart())
async def start_handler(message: Message) -> None:
    """
    Обработчик /start в личке.

    Ты заранее пишешь боту /start, чтобы Telegram разрешил боту
    отправлять тебе личные сообщения.

    В ответ бот покажет твой user_id.
    Его можно вставить в ADMIN_USER_ID в .env.
    """

    user_id = message.from_user.id

    text = (
        "Привет! Я бот для отслеживания вакансий с dobro.ru.\n\n"
        f"Твой Telegram user_id: {user_id}\n\n"
        "Укажи этот ID в .env как ADMIN_USER_ID.\n"
        "После этого я смогу присылать тебе найденные вакансии в личку."
    )

    if user_id != settings.admin_user_id:
        text += (
            "\n\n⚠️ Внимание: сейчас твой user_id не совпадает "
            "с ADMIN_USER_ID из .env."
        )

    await message.answer(text)
