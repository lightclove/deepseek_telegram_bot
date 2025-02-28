
Этот проект представляет собой Telegram-бота, интегрированного с API DeepSeek (на базе OpenAI). Бот позволяет пользователям взаимодействовать с нейросетью, выбирать модели (например, DeepSeek-R1 или DeepSeek-V3) и получать ответы на свои запросы от нейросети импользуя интерфейс мессенджера telegram

Общение с нейросетью: Бот отправляет запросы пользователя в DeepSeek и возвращает ответы.

Управление сессиями: Для каждого пользователя создается отдельная сессия с историей сообщений.

Гибкая настройка: Конфигурация бота (токен, API-ключ, URL) вынесена в .env файл.

## Технологии
Python: Основной язык программирования.

Telegram Bot API: Для взаимодействия с Telegram.

OpenAI API: Для интеграции с DeepSeek.

Systemd: Для запуска бота как сервиса на Linux-сервере.

Dotenv: Для управления конфигурацией через .env файл.

## Установка и настройка
1. Клонирование репозитория

2.Склонируйте репозиторий на ваш сервер
Получите токен для бота в BotFather
3. Настройка .env файла
Создайте файл .env в корне проекта и добавьте туда следующие переменные:
BOT_TOKEN=ваш_токен_бота
API_KEY=ваш_api_ключ
BASE_URL=https://api.proxyapi.ru/openai/v1

4. Запуск бота вручную
Для тестирования запустите бота вручную:
python deepseek_bot.py

5. Запуск как systemd сервиса
1. Создание systemd юнита

Создайте файл сервиса:
sudo nano /etc/systemd/system/deepseek_telegram_bot.service

Добавьте следующую конфигурацию:
[Unit]
Description=Telegram Bot for DeepSeek
After=network.target

[Service]
User=root
WorkingDirectory=/root/deepseek_telegram_bot
ExecStart=/root/deepseek_telegram_bot/venv/bin/python3 /root/deepseek_telegram_bot/deepseek_bot.py
Restart=always
RestartSec=5
Environment="PATH=/root/deepseek_telegram_bot/venv/bin"

[Install]
WantedBy=multi-user.target

2. Перезагрузка systemd и запуск сервиса
Перезагрузите systemd и запустите сервис:
sudo systemctl daemon-reload
sudo systemctl start deepseek_telegram_bot
sudo systemctl enable deepseek_telegram_bot

3. Проверка статуса сервиса
Убедитесь, что сервис работает:
sudo systemctl status deepseek_telegram_bot

Использование бота
Доступные команды
/model: Позволяет выбрать модель для общения (DeepSeek-R1 или DeepSeek-V3).

Любое сообщение: Бот обрабатывает текст и возвращает ответ от выбранной модели.

Пример использования
Отправьте команду /model и выберите модель.

Напишите сообщение, и бот ответит вам, используя выбранную модель.

