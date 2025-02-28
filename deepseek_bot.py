import os
import telebot
from openai import OpenAI
from telebot import types
from dotenv import load_dotenv

# Загрузка переменных окружения из .env файла
load_dotenv()

# Инициализация клиентов с использованием переменных окружения
bot = telebot.TeleBot(os.getenv("BOT_TOKEN"))
client = OpenAI(
    api_key=os.getenv("API_KEY"),
    base_url=os.getenv("BASE_URL")
)

# Хранилище данных пользователей
user_sessions = {}

class UserSession:
    def __init__(self):
        self.model = "deepseek-r1"  # модель по умолчанию
        self.messages = [
            {"role": "system", "content": "You are a helpful assistant."}
        ]

# Обработчик команды /model
@bot.message_handler(commands=['model'])
def set_model(message):
    user_id = message.from_user.id
    if user_id not in user_sessions:
        user_sessions[user_id] = UserSession()

    markup = types.InlineKeyboardMarkup()
    btn_r1 = types.InlineKeyboardButton("DeepSeek-R1", callback_data='model_r1')
    btn_v3 = types.InlineKeyboardButton("DeepSeek-V3", callback_data='model_v3')
    markup.add(btn_r1, btn_v3)

    bot.send_message(
        message.chat.id,
        "Выберите модель для общения:",
        reply_markup=markup
    )

# Обработчик inline кнопок
@bot.callback_query_handler(func=lambda call: call.data.startswith('model_'))
def model_callback(call):
    user_id = call.from_user.id
    model = call.data.split('_')[1]

    if user_id not in user_sessions:
        user_sessions[user_id] = UserSession()

    user_sessions[user_id].model = f"deepseek-{model}"
    bot.send_message(call.message.chat.id, f"✅ Модель изменена на DeepSeek-{model.upper()}")

# Основной обработчик сообщений
@bot.message_handler(func=lambda message: True)
def handle_message(message):
    user_id = message.from_user.id
    if user_id not in user_sessions:
        user_sessions[user_id] = UserSession()

    session = user_sessions[user_id]

    # Добавляем сообщение пользователя в историю
    session.messages.append({"role": "user", "content": message.text})

    try:
        # Отправка запроса в DeepSeek
        response = client.chat.completions.create(
            model="gpt-3.5-turbo-1106" if session.model == "deepseek-r1" else "gpt-4",
            messages=session.messages,
            temperature=0.7
        )

        # Получаем ответ
        assistant_reply = response.choices[0].message.content

        # Добавляем ответ в историю и отправляем
        session.messages.append({"role": "assistant", "content": assistant_reply})
        bot.reply_to(message, assistant_reply)

    except Exception as e:
        bot.reply_to(message, f"⚠️ Произошла ошибка: {str(e)}")
        session.messages.pop()  # Удаляем последнее сообщение

if __name__ == "__main__":
    print("Бот нейросети DeepSeek запущен...")
    bot.infinity_polling()
