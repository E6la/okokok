import re
from dataclasses import dataclass


@dataclass(frozen=True)
class ParsedVacancy:
    """
    Результат парсинга вакансии из сообщения группы.
    """

    position: str
    url: str


# Ищем ссылку на dobro.ru или добро.рф.
# Поддерживает варианты:
# https://dobro.ru/...
# http://dobro.ru/...
# dobro.ru/...
# https://добро.рф/...
DOBRO_URL_RE = re.compile(
    r"(?P<url>(?:https?://)?(?:www\.)?(?:dobro\.ru|добро\.рф)/[^\s<>\]\)\"']+)",
    re.IGNORECASE,
)

# Ищем строку вида:
# Должность: Волонтёр
# Должность: Координатор мероприятия
POSITION_RE = re.compile(
    r"^\s*Должность\s*:\s*(?P<position>.+?)\s*$",
    re.IGNORECASE | re.MULTILINE,
)


def normalize_url(url: str) -> str:
    """
    Telegram-кнопке с url лучше давать полную ссылку с https://.
    Если в сообщении было просто dobro.ru/..., добавим https:// сами.
    """

    url = url.strip().rstrip(".,;!?")

    if not url.startswith(("http://", "https://")):
        url = "https://" + url

    return url


def parse_vacancy(text: str) -> ParsedVacancy | None:
    """
    Главная функция парсинга.

    Принимает текст сообщения из группы.
    Возвращает ParsedVacancy, если нашли и ссылку, и должность.
    Если чего-то нет — возвращает None.
    """

    url_match = DOBRO_URL_RE.search(text)
    position_match = POSITION_RE.search(text)

    if not url_match or not position_match:
        return None

    url = normalize_url(url_match.group("url"))
    position = position_match.group("position").strip()

    if not position:
        return None

    return ParsedVacancy(position=position, url=url)
