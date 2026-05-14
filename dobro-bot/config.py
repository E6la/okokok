import os
from dataclasses import dataclass

from dotenv import load_dotenv


@dataclass(frozen=True)
class Settings:
    """
    Здесь храним настройки бота.

    BOT_TOKEN — токен бота от BotFather.
    TARGET_GROUP_ID — ID группы, откуда бот читает вакансии.
    ADMIN_USER_ID — твой Telegram user_id, куда бот шлёт личные сообщения.
    """

    bot_token: str
    target_group_id: int
    admin_user_id: int


def load_settings() -> Settings:
    """
    Загружаем переменные из .env и проверяем, что всё нужное есть.
    """

    load_dotenv()

    bot_token = os.getenv("BOT_TOKEN")
    target_group_id = os.getenv("TARGET_GROUP_ID")
    admin_user_id = os.getenv("ADMIN_USER_ID")

    if not bot_token:
        raise RuntimeError("Не задан BOT_TOKEN в .env")

    if not target_group_id:
        raise RuntimeError("Не задан TARGET_GROUP_ID в .env")

    if not admin_user_id:
        raise RuntimeError("Не задан ADMIN_USER_ID в .env")

    return Settings(
        bot_token=bot_token,
        target_group_id=int(target_group_id),
        admin_user_id=int(admin_user_id),
    )


settings = load_settings()
