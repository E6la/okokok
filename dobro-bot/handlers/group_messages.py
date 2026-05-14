import logging

from aiogram import Bot, Router
from aiogram.exceptions import TelegramBadRequest, TelegramForbiddenError
from aiogram.types import Message

from config import settings
from keyboards.inline import vacancy_confirm_keyboard
from services.parser import parse_vacancy
from storage import save_vacancy

router = Router(name=__name__)

logger = logging.getLogger(__name__)


@router.message()
async def group_message_handler(message: Message, bot: Bot) -> None:
    """
    Обработчик всех сообщений.

    Логика:
    1. Проверяем, что сообщение пришло именно из нужной группы.
    2. Берём текст сообщения или подпись к медиа.
    3. Ищем ссылку на dobro.ru.
    4. Ищем строку Должность: ...
    5. Если всё нашли — отправляем админу личное сообщение с кнопками.

    В группу бот ничего не пишет.
    """

    # Если сообщение не из нужной группы — просто игнорируем.
    if message.chat.id != settings.target_group_id:
        return

    # Вакансия может быть обычным текстом или подписью к картинке/файлу.
    text = message.text or message.caption

    if not text:
        return

    parsed = parse_vacancy(text)

    # Если нет ссылки на dobro.ru или нет строки "Должность:", ничего не делаем.
    if parsed is None:
        return

    vacancy = save_vacancy(
        position=parsed.position,
        url=parsed.url,
        source_chat_id=message.chat.id,
        source_message_id=message.message_id,
    )

    private_text = (
        f"Нашёл вакансию: {vacancy.position}\n"
        f"Ссылка: {vacancy.url}\n\n"
        "Подать заявку на эту вакансию?"
    )

    try:
        await bot.send_message(
            chat_id=settings.admin_user_id,
            text=private_text,
            reply_markup=vacancy_confirm_keyboard(vacancy.id),
        )

        logger.info(
            "Нашёл вакансию '%s' и отправил админу",
            vacancy.position,
        )

    except TelegramForbiddenError:
        logger.error(
            "Не могу написать админу. Сначала напиши боту /start в личке."
        )

    except TelegramBadRequest as error:
        logger.error("Ошибка при отправке личного сообщения: %s", error)
