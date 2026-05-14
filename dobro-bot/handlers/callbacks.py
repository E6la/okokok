from aiogram import F, Router
from aiogram.types import CallbackQuery

from config import settings
from keyboards.inline import open_vacancy_keyboard
from storage import delete_vacancy, get_vacancy

router = Router(name=__name__)


@router.callback_query(F.data.startswith("apply:"))
async def apply_callback_handler(callback: CallbackQuery) -> None:
    """
    Обработка кнопки "Да, подать".

    Бот НЕ отправляет ничего на dobro.ru.
    Он только даёт кнопку-ссылку, чтобы ты сам открыл страницу.
    """

    if callback.from_user.id != settings.admin_user_id:
        await callback.answer("Эта кнопка не для вас.", show_alert=True)
        return

    vacancy_id = callback.data.split(":", maxsplit=1)[1]
    vacancy = get_vacancy(vacancy_id)

    if vacancy is None:
        await callback.answer(
            "Вакансия не найдена. Возможно, бот был перезапущен.",
            show_alert=True,
        )
        return

    # На callback нужно обязательно ответить,
    # иначе в Telegram будет крутиться индикатор загрузки.
    await callback.answer()

    await callback.message.answer(
        text=f'Окей, вот ссылка для подачи заявки на "{vacancy.position}"',
        reply_markup=open_vacancy_keyboard(vacancy.url),
    )

    # Убираем старые кнопки Да/Нет, чтобы случайно не нажимать повторно.
    await callback.message.edit_reply_markup(reply_markup=None)

    delete_vacancy(vacancy_id)


@router.callback_query(F.data.startswith("skip:"))
async def skip_callback_handler(callback: CallbackQuery) -> None:
    """
    Обработка кнопки "Нет, пропустить".
    """

    if callback.from_user.id != settings.admin_user_id:
        await callback.answer("Эта кнопка не для вас.", show_alert=True)
        return

    vacancy_id = callback.data.split(":", maxsplit=1)[1]

    await callback.answer("Ок, пропускаю.")

    await callback.message.edit_text("Ок, пропускаю эту вакансию.")

    delete_vacancy(vacancy_id)
