#!/usr/bin/env bash
# Установка бота как systemd-сервиса на Ubuntu/Debian.
# Запуск на сервере: sudo bash deploy/install.sh
set -euo pipefail

APP_DIR=/opt/okokok/dobro-bot
REPO_URL=https://github.com/e6la/okokok.git

apt-get update -y
apt-get install -y git python3 python3-venv

if [ ! -d /opt/okokok ]; then
    git clone "$REPO_URL" /opt/okokok
else
    git -C /opt/okokok pull --ff-only
fi

cd "$APP_DIR"
python3 -m venv .venv
.venv/bin/pip install --upgrade pip
.venv/bin/pip install -r requirements.txt

if [ ! -f .env ]; then
    cp .env.example .env
    echo "Заполни $APP_DIR/.env и запусти скрипт ещё раз."
    exit 1
fi

cp deploy/dobro-bot.service /etc/systemd/system/dobro-bot.service
systemctl daemon-reload
systemctl enable --now dobro-bot
systemctl restart dobro-bot
systemctl --no-pager status dobro-bot
