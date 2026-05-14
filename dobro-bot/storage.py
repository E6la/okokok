from dataclasses import dataclass
from uuid import uuid4


@dataclass
class Vacancy:
    """
    Вакансия, которую бот нашёл в группе.

    Важно:
    callback_data у Telegram маленькая, поэтому длинную ссылку туда не кладём.
    Вместо этого сохраняем вакансию в памяти, а в кнопку кладём короткий vacancy_id.
    """

    id: str
    position: str
    url: str
    source_chat_id: int
    source_message_id: int


# Простое хранилище в памяти.
# Если бот перезапустить, данные пропадут.
# Для серьёзного проекта можно заменить на SQLite/PostgreSQL.
VACANCIES: dict[str, Vacancy] = {}


def save_vacancy(
    position: str,
    url: str,
    source_chat_id: int,
    source_message_id: int,
) -> Vacancy:
    """
    Сохраняем вакансию и возвращаем объект Vacancy.
    """

    vacancy_id = uuid4().hex[:12]

    vacancy = Vacancy(
        id=vacancy_id,
        position=position,
        url=url,
        source_chat_id=source_chat_id,
        source_message_id=source_message_id,
    )

    VACANCIES[vacancy_id] = vacancy
    return vacancy


def get_vacancy(vacancy_id: str) -> Vacancy | None:
    """
    Получаем вакансию по короткому ID.
    """

    return VACANCIES.get(vacancy_id)


def delete_vacancy(vacancy_id: str) -> None:
    """
    Удаляем вакансию из памяти, например после нажатия Да/Нет.
    """

    VACANCIES.pop(vacancy_id, None)
