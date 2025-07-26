import os
import logging
from aiogram import Bot, Dispatcher, types
from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils import executor
import sqlite3
from datetime import datetime

TEST_MODE = True
TEST_CHAT_ID = 345470935
CHANNEL_CHAT_ID = -1002510932658
ADMIN_ID = 345470935

# Настройка логов
logging.basicConfig(level=logging.INFO)

# Массив посланий для вечера 25 июля
interactive_evening_cards = [
    "✨ Вечер 25 июля. Открой сердце навстречу теплу и свету. Пусть интуиция ведёт тебя к радости и гармонии.",
    "🌙 Вечер 25 июля. Позволь себе отдохнуть и наполниться вдохновением. Ты заслуживаешь покоя и счастья.",
    "💫 Вечер 25 июля. Верь в свои силы и мечты. Сегодня звёзды поддерживают твой путь к исполнению желаний.",
    "🌟 Вечер 25 июля. Оставь тревоги позади. Пусть душа наполнится светом и любовью, а сердце — уверенностью.",
    "🔥 Вечер 25 июля. Разжигай внутренний огонь и смело иди вперёд. Ты способен на большее, чем думаешь.",
    "🌈 Вечер 25 июля. Пусть этот вечер принесёт тебе мир и радость. Откройся новым возможностям и счастью."
]

# Получение токена из переменных окружения
BOT_TOKEN = "7926255775:AAH3YnN9IwtSBcpLxgasi6NHScQKV1D194w"

# Создание бота и диспетчера
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher(bot)

# Инициализация базы данных
conn = sqlite3.connect('bot_database.db')
cursor = conn.cursor()
cursor.execute('''
CREATE TABLE IF NOT EXISTS user_choices (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    choice TEXT NOT NULL,
    date TEXT NOT NULL
)
''')
conn.commit()

# Команда /start
@dp.message_handler(commands=["start"])
async def start(message: Message):
    # Главное меню с новой кнопкой "🌅 Доброе утро"
    keyboard = ReplyKeyboardMarkup(
        keyboard=[
            ["🃏 Карта дня", "🌟 Гороскоп"],
            ["🌙 Вечернее послание"],
            ["🔮 Интерактив"],
            ["💘 Совместимость знаков"],
            ["🌅 Доброе утро"]
        ],
        resize_keyboard=True
    )
    await message.answer("👋 Привет! Бот запущен и готов к работе.", reply_markup=keyboard)

# Команда /help
@dp.message_handler(commands=["help"])
async def help_command(message: Message):
    await message.answer("Доступные команды:\n/start - Запустить бота\n/help - Помощь\n/cards - Показать карты")

# Команда /cards
@dp.message_handler(commands=["cards"])
async def cards_command(message: Message):
    await message.answer("Здесь будут ваши карты.")

# Команды для переключения режима
@dp.message_handler(commands=["test"])
async def set_test_mode(message: Message):
    global TEST_MODE
    TEST_MODE = True
    await message.answer("Режим публикаций: тестовый")

@dp.message_handler(commands=["prod"])
async def set_prod_mode(message: Message):
    global TEST_MODE
    TEST_MODE = False
    await message.answer("Режим публикаций: рабочий")

# Обработчик сообщений
@dp.message_handler()
async def handle_message(message: Message):
    if message.text == "🔮 Интерактив":
        keyboard = InlineKeyboardMarkup(row_width=3)
        buttons = [InlineKeyboardButton(text=f"Карта {i+1}", callback_data=f"interactive_card_{i+1}") for i in range(6)]
        keyboard.add(*buttons)
        # Отправляем предпросмотр только админу
        preview_caption = "✨ ПРЕДПРОСМОТР публикации интерактива на сегодня:\n\n⚠️ Подтверди публикацию или отмени."
        preview_keyboard = InlineKeyboardMarkup(row_width=2)
        preview_keyboard.add(
            InlineKeyboardButton(text="✅ Опубликовать в канал", callback_data="publish_confirm"),
            InlineKeyboardButton(text="❌ Отмена", callback_data="publish_cancel")
        )
        photo_path = "/Users/konstantinbaranov/Desktop/images/всвоюсилу.jpg"
        with open(photo_path, "rb") as photo:
            await bot.send_photo(
                chat_id=ADMIN_ID,
                photo=photo,
                caption=preview_caption,
                reply_markup=preview_keyboard
            )
        await message.answer("Пост для проверки отправлен админу!")
    elif message.text == "/best_pairs" or message.text == "Лучшие пары знаков":
        bestpairs_caption = (
            "✨ Лучшие пары знаков на этот уикенд!\n\n"
            "Каждый знак и его наилучшее романтическое сочетание по Таро и эзотерике на эти выходные:\n\n"
            "♈ Овен — Лев  \n"
            "♉ Телец — Козерог  \n"
            "♊ Близнецы — Водолей  \n"
            "♋ Рак — Рыбы  \n"
            "♌ Лев — Весы  \n"
            "♍ Дева — Телец  \n"
            "♎ Весы — Близнецы  \n"
            "♏ Скорпион — Козерог  \n"
            "♐ Стрелец — Овен  \n"
            "♑ Козерог — Телец  \n"
            "♒ Водолей — Близнецы  \n"
            "♓ Рыбы — Рак  \n\n"
            "💖 Пусть этот уикенд принесёт новые чувства и взаимные откровения!"
        )
        preview_keyboard = InlineKeyboardMarkup(row_width=2)
        preview_keyboard.add(
            InlineKeyboardButton(text="✅ Опубликовать в канал", callback_data="bestpairs_confirm"),
            InlineKeyboardButton(text="❌ Отмена", callback_data="bestpairs_cancel")
        )
        await bot.send_message(
            chat_id=ADMIN_ID,
            text=bestpairs_caption,
            reply_markup=preview_keyboard
        )
        await message.answer("Пост для проверки отправлен админу!")
    elif message.text == "🌅 Доброе утро":
        preview_text = (
            "✨ Доброе утро!\n\n"
            "Пусть день принесёт вдохновение, лёгкость и новые добрые открытия. "
            "Улыбнись утру и доверься потоку дня! 🌞"
        )
        # Кнопки: "✨ Тебе послание", "❤️", "🙏", "🥹" в одной структуре
        morning_keyboard = InlineKeyboardMarkup(row_width=3)
        morning_keyboard.add(
            InlineKeyboardButton(text="✨ Тебе послание", callback_data="morning_msg")
        )
        morning_keyboard.add(
            InlineKeyboardButton(text="❤️", callback_data="morning_react_heart"),
            InlineKeyboardButton(text="🙏", callback_data="morning_react_pray"),
            InlineKeyboardButton(text="🥹", callback_data="morning_react_cute")
        )
        morning_keyboard.add(
            InlineKeyboardButton(text="❓ Задать вопрос", url="https://t.me/exo_fruit")
        )
        await message.answer(preview_text, reply_markup=morning_keyboard)
    elif message.text == "🌟 Гороскоп":
        # Предпросмотр поста "Гороскоп на сегодня 26 июля" только админу
        preview_caption = (
            "🌟 <b>Гороскоп на сегодня 26 июля</b>\n\n"
            "Выбери свой знак, чтобы получить индивидуальное послание на день. "
            "Дополнительно доступны: послание от Проводницы, ритуал и аффирмация дня."
        )
        # Новый блок: 12 знаков зодиака в 4 строки по 3, формат "СИМВОЛ Название"
        zodiac_names = {
            "aries": "♈ Овен", "taurus": "♉ Телец", "gemini": "♊ Близнецы", "cancer": "♋ Рак",
            "leo": "♌ Лев", "virgo": "♍ Дева", "libra": "♎ Весы", "scorpio": "♏ Скорпион",
            "sagittarius": "♐ Стрелец", "capricorn": "♑ Козерог", "aquarius": "♒ Водолей", "pisces": "♓ Рыбы"
        }
        zodiac_keys = list(zodiac_names.keys())
        zodiac_buttons = [InlineKeyboardButton(zodiac_names[key], callback_data=f"horoscope_{key}") for key in zodiac_keys]
        inline_buttons = [zodiac_buttons[i:i+3] for i in range(0, 12, 3)]
        # Блок из трёх кнопок под зодиаками
        inline_buttons.append([
            InlineKeyboardButton("✨ Послание от Проводницы", callback_data="conductor_msg"),
            InlineKeyboardButton("🔮 Ритуал дня", callback_data="ritual_msg"),
            InlineKeyboardButton("🌱 Аффирмация дня", callback_data="affirmation_msg"),
        ])
        # Кнопка "Задать вопрос?"
        inline_buttons.append([
            InlineKeyboardButton("Задать вопрос?", url="https://t.me/exo_fruit")
        ])
        # Кнопки предпросмотра и подтверждения для админа
        preview_keyboard = InlineKeyboardMarkup(inline_buttons + [
            [
                InlineKeyboardButton("✅ Опубликовать в канал", callback_data="horoscope_confirm"),
                InlineKeyboardButton("❌ Отмена", callback_data="horoscope_cancel")
            ]
        ])
        await bot.send_message(
            chat_id=ADMIN_ID,
            text=preview_caption,
            parse_mode="HTML",
            reply_markup=preview_keyboard
        )
        await message.answer("Пост для проверки отправлен админу!")
    else:
        await message.answer(f"Ты написал: {message.text}")

# Обработчик callback_query (если используется)
@dp.callback_query_handler()
async def handle_callback(callback_query: types.CallbackQuery):
    data = callback_query.data
    user_id = callback_query.from_user.id
    today_str = datetime.now().strftime("%Y-%m-%d")
    # --- Гороскоп и вечерние сообщения ---
    day_messages = {
        "aries": "♈ Овен — Сегодня день новых начинаний. Откройся возможностям и не бойся выделяться.",
        "taurus": "♉ Телец — Спокойствие и стабильность приведут к результату. Позволь себе радость в простом.",
        "gemini": "♊ Близнецы — Новости и встречи подарят вдохновение. Используй слово как инструмент.",
        "cancer": "♋ Рак — Забота о себе принесёт гармонию. Поделись теплом с близкими.",
        "leo": "♌ Лев — Прояви творческий подход. Яркие идеи будут замечены!",
        "virgo": "♍ Дева — В деталях кроется успех. Сегодня особенно полезны порядок и анализ.",
        "libra": "♎ Весы — Гармония отношений — твой ресурс дня. Не избегай честного разговора.",
        "scorpio": "♏ Скорпион — Трансформация дня даст новый опыт. Не бойся перемен.",
        "sagittarius": "♐ Стрелец — Возможны неожиданные предложения. Прими их с любопытством.",
        "capricorn": "♑ Козерог — Структура и план приведут к цели. Вечером удели внимание семье.",
        "aquarius": "♒ Водолей — Вдохновение приходит в уединении. Обрати внимание на свои идеи.",
        "pisces": "♓ Рыбы — Вода дня очищает чувства. Позволь мечтам вести тебя."
    }
    evening_messages = {
        "aries": "Сегодня прояви инициативу — твоя энергия заразительна. Люди вокруг готовы поддержать твои идеи. Верь в себя и открывай новые возможности!",
        "taurus": "Сосредоточься на деталях и домашних делах. Маленькие шаги принесут большое удовлетворение. Побалуй себя чем-то приятным, ты этого заслуживаешь!",
        "gemini": "Впереди день встреч и ярких разговоров. Делись мыслями, слушай других и не бойся новых знакомств. Откройся переменам — они подарят вдохновение!",
        "cancer": "Сделай акцент на заботе о себе и близких. День благоприятен для уюта, теплых слов и творческих занятий. Отпусти старые тревоги и поверь в лучшее.",
        "leo": "Твоя харизма сегодня на пике! Устрой себе маленький праздник, порадуй близких и получи заслуженное внимание. Действуй с радостью и смелостью.",
        "virgo": "Планируй и наводи порядок в мыслях и делах. Сегодня особенно полезны списки и здоровые привычки. Позволь себе отдохнуть вечером в тишине.",
        "libra": "Гармония отношений — главный ресурс дня. Откровенный разговор поможет разрешить сомнения. Найди баланс между работой и личной жизнью.",
        "scorpio": "Интуиция подскажет лучший путь. Не бойся перемен — они приведут к внутренней силе. Слушай себя и доверяй внутреннему голосу.",
        "sagittarius": "День хорош для новых идей, путешествий и учебы. Откройся опыту и не ограничивай себя рамками. Друзья и союзники помогут воплотить планы.",
        "capricorn": "Достигай целей шаг за шагом. Сегодня в приоритете дисциплина и забота о семье. Радуйся маленьким успехам — это твой фундамент будущего.",
        "aquarius": "Вдохновение приходит в одиночестве. Не бойся уединения, оно откроет новые грани твоей души. Делись открытиями с теми, кто тебе близок.",
        "pisces": "Творчество и мечты ведут тебя сегодня. Позволь себе плыть по течению, доверяй эмоциям и не стесняйся мечтать вслух — Вселенная тебя слышит."
    }
    conductor_message = "✨ Послание от Проводницы:\n\nПозволь себе быть мягкой и принимать заботу. Всё нужное уже рядом — просто замедлись и почувствуй."
    ritual_message = "🔮 Ритуал дня:\n\nЗажги свечу утром или вечером, сформулируй вслух своё главное желание на день. Вдохни глубоко, представь, как оно уже исполнилось."
    affirmation_message = "🌱 Аффирмация дня:\n\n«Я достойна любви, поддержки и радости. Всё, что мне нужно, приходит легко и вовремя.»"
    if data and data.startswith("interactive_card_"):
        # Проверяем, тянул ли пользователь карту сегодня
        cursor.execute("SELECT 1 FROM user_choices WHERE user_id = ? AND choice LIKE 'interactive_card_%' AND date = ?", (user_id, today_str))
        already_drawn = cursor.fetchone()
        if already_drawn:
            await callback_query.answer("Сегодня ты уже тянула карту! Попробуй завтра.", show_alert=True)
        else:
            index = int(data.split("_")[-1]) - 1
            if 0 <= index < len(interactive_evening_cards):
                # Сохраняем выбор
                cursor.execute("INSERT INTO user_choices (user_id, choice, date) VALUES (?, ?, ?)", (user_id, data, today_str))
                conn.commit()
                # Отвечаем с посланием и убираем кнопки
                await callback_query.answer(interactive_evening_cards[index], show_alert=True)
                await bot.edit_message_text(
                    chat_id=callback_query.message.chat.id,
                    message_id=callback_query.message.message_id,
                    text="✨ Ты вытянул карту на сегодня. Возвращайся завтра за новым посланием!"
                )
            else:
                await callback_query.answer("Неверный выбор карты.")
    elif data == "publish_confirm" and user_id == ADMIN_ID:
        keyboard = InlineKeyboardMarkup(row_width=3)
        buttons = [InlineKeyboardButton(text=f"Карта {i+1}", callback_data=f"interactive_card_{i+1}") for i in range(6)]
        keyboard.add(*buttons)
        photo_path = "/Users/konstantinbaranov/Desktop/images/всвоюсилу.jpg"
        with open(photo_path, "rb") as photo:
            sent_message = await bot.send_photo(
                chat_id=CHANNEL_CHAT_ID,
                photo=photo,
                caption="✨ Выбери одну из 6 карт на вечер пятницы 25 июля.\n\n⚠️ Важно: вытянуть карту можно только один раз!",
                reply_markup=keyboard
            )
        await bot.edit_message_caption(
            chat_id=callback_query.message.chat.id,
            message_id=callback_query.message.message_id,
            caption="✅ Публикация выполнена! Пост ушёл в канал.",
            reply_markup=None
        )
        await callback_query.answer("Пост опубликован в канал!", show_alert=True)
    elif data == "publish_cancel" and user_id == ADMIN_ID:
        await bot.edit_message_caption(
            chat_id=callback_query.message.chat.id,
            message_id=callback_query.message.message_id,
            caption="❌ Публикация отменена.",
            reply_markup=None
        )
        await callback_query.answer("Публикация отменена.", show_alert=True)
    elif data == "bestpairs_confirm" and user_id == ADMIN_ID:
        bestpairs_caption = (
            "✨ Лучшие пары знаков на этот уикенд!\n\n"
            "Каждый знак и его наилучшее романтическое сочетание по Таро и эзотерике на эти выходные:\n\n"
            "♈ Овен — Лев  \n"
            "♉ Телец — Козерог  \n"
            "♊ Близнецы — Водолей  \n"
            "♋ Рак — Рыбы  \n"
            "♌ Лев — Весы  \n"
            "♍ Дева — Телец  \n"
            "♎ Весы — Близнецы  \n"
            "♏ Скорпион — Козерог  \n"
            "♐ Стрелец — Овен  \n"
            "♑ Козерог — Телец  \n"
            "♒ Водолей — Близнецы  \n"
            "♓ Рыбы — Рак  \n\n"
            "💖 Пусть этот уикенд принесёт новые чувства и взаимные откровения!"
        )
        await bot.send_message(
            chat_id=CHANNEL_CHAT_ID,
            text=bestpairs_caption
        )
        await bot.edit_message_text(
            chat_id=callback_query.message.chat.id,
            message_id=callback_query.message.message_id,
            text="✅ Публикация выполнена! Пост ушёл в канал.",
            reply_markup=None
        )
        await callback_query.answer("Пост опубликован в канал!", show_alert=True)
    elif data == "bestpairs_cancel" and user_id == ADMIN_ID:
        await bot.edit_message_text(
            chat_id=callback_query.message.chat.id,
            message_id=callback_query.message.message_id,
            text="❌ Публикация отменена.",
            reply_markup=None
        )
        await callback_query.answer("Публикация отменена.", show_alert=True)
    elif data == "morning_msg":
        import random
        morning_messages = [
            "✨ Пусть сегодня для тебя откроется новый источник вдохновения!",
            "🌞 Новый день — новые чудеса. Пусть сердце радуется каждому мгновению.",
            "🌸 Позволь себе радоваться простым вещам. Пусть сегодня всё получится легко!",
            "🦋 Пусть в этот день откроются новые возможности для счастья.",
            "☕️ С добрым утром! Пусть мысли будут светлыми, а дела успешными.",
            "🌿 Доверяй себе — сегодня твой внутренний голос особенно ярок.",
            "🌺 Пусть в твою жизнь войдёт забота, поддержка и искренние улыбки.",
            "🪐 Этот день создан для твоих побед. Дерзай!",
            "🌼 Пусть на душе будет тепло, а сердце наполнится благодарностью.",
            "💫 Всё получится! Вселенная рядом, поддержка внутри тебя."
        ]
        msg = random.choice(morning_messages)
        await callback_query.answer(msg, show_alert=True)
        return
    elif data == "morning_react_heart":
        await callback_query.answer("Спасибо за реакцию! ❤️", show_alert=True)
        return
    elif data == "morning_react_pray":
        await callback_query.answer("Спасибо за светлую энергию! 🙏", show_alert=True)
        return
    elif data == "morning_react_cute":
        await callback_query.answer("Спасибо за доброту! 🥹", show_alert=True)
        return
    elif data == "horoscope_confirm" and user_id == ADMIN_ID:
        # Публикация поста "Гороскоп на сегодня 26 июля" в канал (в 3 столбца по 4 строки)
        pub_caption = (
            "🌟 <b>Гороскоп на сегодня 26 июля</b>\n\n"
            "Выбери свой знак, чтобы получить индивидуальное послание на день. "
            "Дополнительно доступны: послание от Проводницы, ритуал и аффирмация дня."
        )
        zodiac_names = {
            "aries": "♈ Овен", "taurus": "♉ Телец", "gemini": "♊ Близнецы", "cancer": "♋ Рак",
            "leo": "♌ Лев", "virgo": "♍ Дева", "libra": "♎ Весы", "scorpio": "♏ Скорпион",
            "sagittarius": "♐ Стрелец", "capricorn": "♑ Козерог", "aquarius": "♒ Водолей", "pisces": "♓ Рыбы"
        }
        zodiac_keys = list(zodiac_names.keys())
        zodiac_buttons = [InlineKeyboardButton(zodiac_names[key], callback_data=f"horoscope_{key}") for key in zodiac_keys]
        inline_buttons = [zodiac_buttons[i:i+3] for i in range(0, 12, 3)]
        # Блок из трёх кнопок под зодиаками
        inline_buttons.append([
            InlineKeyboardButton("✨ Послание от Проводницы", callback_data="conductor_msg"),
            InlineKeyboardButton("🔮 Ритуал дня", callback_data="ritual_msg"),
            InlineKeyboardButton("🌱 Аффирмация дня", callback_data="affirmation_msg"),
        ])
        # Кнопка "Задать вопрос?"
        inline_buttons.append([
            InlineKeyboardButton("Задать вопрос?", url="https://t.me/exo_fruit")
        ])
        pub_keyboard = InlineKeyboardMarkup(inline_buttons)
        await bot.send_message(
            chat_id=CHANNEL_CHAT_ID,
            text=pub_caption,
            parse_mode="HTML",
            reply_markup=pub_keyboard
        )
        await bot.edit_message_text(
            chat_id=callback_query.message.chat.id,
            message_id=callback_query.message.message_id,
            text="✅ Публикация выполнена! Пост ушёл в канал.",
            reply_markup=None
        )
        await callback_query.answer("Пост опубликован в канал!", show_alert=True)
    elif data == "horoscope_cancel" and user_id == ADMIN_ID:
        await bot.edit_message_text(
            chat_id=callback_query.message.chat.id,
            message_id=callback_query.message.message_id,
            text="❌ Публикация отменена.",
            reply_markup=None
        )
        await callback_query.answer("Публикация отменена.", show_alert=True)
    elif data and data.startswith("horoscope_"):
        sign = data.replace("horoscope_", "")
        msg = day_messages.get(sign)
        if msg:
            await callback_query.answer(msg, show_alert=True)
        else:
            await callback_query.answer("Неизвестный знак.", show_alert=True)
    elif data == "conductor_msg":
        await callback_query.answer(conductor_message, show_alert=True)
    elif data == "ritual_msg":
        await callback_query.answer(ritual_message, show_alert=True)
    elif data == "affirmation_msg":
        await callback_query.answer(affirmation_message, show_alert=True)
    else:
        await callback_query.answer("Обработан callback")

# Запуск бота
if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)

    elif data and data.startswith("evening_zodiac_"):
        sign = data.replace("evening_zodiac_", "")
        msg = evening_messages.get(sign)
        if msg:
            await callback_query.answer(msg, show_alert=True)
        else:
            await callback_query.answer("Неизвестный знак.", show_alert=True)