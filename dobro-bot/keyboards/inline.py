from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


def vacancy_confirm_keyboard(vacancy_id: str) -> InlineKeyboardMarkup:
    """
    Клавиатура для личного сообщения:
    Да — подать заявку.
    Нет — пропустить.
    """

    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="Да, подать",
                    callback_data=f"apply:{vacancy_id}",
                )
            ],
            [
                InlineKeyboardButton(
                    text="Нет, пропустить",
                    callback_data=f"skip:{vacancy_id}",
                )
            ],
        ]
    )


def open_vacancy_keyboard(url: str) -> InlineKeyboardMarkup:
    """
    Кнопка-ссылка, которая открывает страницу dobro.ru в браузере.
    """

    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="Открыть страницу на dobro.ru",
                    url=url,
                )
            ]
        ]
    )
