# dobro-bot

Telegram-бот: читает сообщения в группе, находит вакансии со ссылкой на dobro.ru
и строкой `Должность: ...`, и присылает их админу в личку с кнопками «Да / Нет».

## Подготовка

1. Создай бота у [@BotFather](https://t.me/BotFather) (`/newbot`) и скопируй токен.
2. У BotFather: `/setprivacy` → выбери бота → **Disable**, иначе бот не увидит сообщения в группе.
3. Добавь бота в группу с вакансиями.
4. Скопируй `.env.example` в `.env` и заполни `BOT_TOKEN`, `TARGET_GROUP_ID`, `ADMIN_USER_ID`.
   - `ADMIN_USER_ID` бот покажет в ответ на `/start` в личке.
   - `TARGET_GROUP_ID` можно узнать, например, через [@getmyid_bot](https://t.me/getmyid_bot) или из логов.
5. Напиши боту `/start` в личке, чтобы он мог присылать тебе сообщения.

## Запуск на сервере

### Вариант 1: Docker

```bash
git clone https://github.com/e6la/okokok.git
cd okokok/dobro-bot
cp .env.example .env && nano .env
docker compose up -d --build
docker compose logs -f
```

### Вариант 2: systemd (Ubuntu/Debian)

```bash
sudo bash -c "$(curl -fsSL https://raw.githubusercontent.com/e6la/okokok/main/dobro-bot/deploy/install.sh)"
sudo nano /opt/okokok/dobro-bot/.env
sudo bash /opt/okokok/dobro-bot/deploy/install.sh
journalctl -u dobro-bot -f
```

## Локальный запуск

```bash
python3 -m venv .venv
.venv/bin/pip install -r requirements.txt
.venv/bin/python bot.py
```
