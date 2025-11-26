#!/bin/bash

TOKENS_FILE = "tokens.txt"

# Если передан аргумент - используем его, иначе берем случайный из файла
if [-n "$1"]; then
TOKEN = "$1"
echo
"🔄 Запускаю бота с переданным токеном..."
else
# Проверяем существование файла с токенами
if [ ! -f "$TOKENS_FILE"]; then
echo
"❌ Файл $TOKENS_FILE не найден"
echo
"💡 Создайте файл $TOKENS_FILE со списком токенов"
echo
"💡 Или используйте: ./run-bot.sh <ваш_токен>"
exit
1
fi

# Выбираем случайный токен
TOKEN =$(shuf - n 1 "$TOKENS_FILE")
echo
"🔄 Запускаю бота со случайным токеном из $TOKENS_FILE..."
fi

echo
"⏳ Останавливаю старый контейнер..."
docker
rm - f
my - bot
2 > / dev / null

echo
"🚀 Запускаю новый контейнер..."
docker
run - d - -name
my - bot - e
TELEGRAM_BOT_TOKEN = "$TOKEN"
my - telegram - bot

echo
"✅ Бот запущен!"
echo
"📋 Токен (первые 10 символов): ${TOKEN:0:10}..."
echo
"📊 Для просмотра логов: docker logs my-bot"
echo
"🛑 Для остановки: docker stop my-bot"
