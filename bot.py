from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import Updater, CommandHandler, CallbackContext, CallbackQueryHandler
import logging
import os

TOKEN = os.environ.get("BOT_TOKEN")
CHANNEL_USERNAME = "@eto_vse_ty"

logging.basicConfig(level=logging.INFO)

messages = {
    'aries': "♈ Овен: Отпусти борьбу. Сегодня ты просто свет. Пусть ночь унесёт тревоги.",
    'taurus': "♉ Телец: Ты заслужил(а) покой. Земля под тобой, небо над тобой — ты в безопасности.",
    'gemini': "♊ Близнецы: Мысли затихают. Пусть звёзды шепчут, а ты слушаешь сны.",
    'cancer': "♋ Рак: Ночь — дом твоей души. Позволь себе укрыться в её тишине.",
    'leo': "♌ Лев: Твоя сила отдыхает. Завтра ты снова солнце, а сегодня — луна.",
    'virgo': "♍ Дева: Ты всё уладишь — но не сейчас. Сейчас — только дыхание и звёзды.",
    'libra': "♎ Весы: Всё в равновесии. Ты можешь выдохнуть и довериться ночи.",
    'scorpio': "♏ Скорпион: Сегодня не нужно глубоко. Достаточно просто быть и дышать.",
    'sagittarius': "♐ Стрелец: Завтра путь продолжится. А сегодня — пусть будет отдых.",
    'capricorn': "♑ Козерог: Не контролируй ночь. Она мудрее. Она знает, как тебя исцелить.",
    'aquarius': "♒ Водолей: Ты был светом. Сейчас будь покоем. Завтра снова сияй.",
    'pisces': "♓ Рыбы: Сны уже ждут тебя. Плыви к ним, не спрашивая зачем."
}

def start(update: Update, context: CallbackContext):
    user_id = update.effective_user.id
    chat_member = context.bot.get_chat_member(chat_id=CHANNEL_USERNAME, user_id=user_id)

    if chat_member.status in ['member', 'administrator', 'creator']:
        keyboard = [
            [InlineKeyboardButton("♈ Овен", callback_data='aries'), InlineKeyboardButton("♉ Телец", callback_data='taurus')],
            [InlineKeyboardButton("♊ Близнецы", callback_data='gemini'), InlineKeyboardButton("♋ Рак", callback_data='cancer')],
            [InlineKeyboardButton("♌ Лев", callback_data='leo'), InlineKeyboardButton("♍ Дева", callback_data='virgo')],
            [InlineKeyboardButton("♎ Весы", callback_data='libra'), InlineKeyboardButton("♏ Скорпион", callback_data='scorpio')],
            [InlineKeyboardButton("♐ Стрелец", callback_data='sagittarius'), InlineKeyboardButton("♑ Козерог", callback_data='capricorn')],
            [InlineKeyboardButton("♒ Водолей", callback_data='aquarius'), InlineKeyboardButton("♓ Рыбы", callback_data='pisces')],
        ]
        update.message.reply_text("Выбери свой знак зодиака:", reply_markup=InlineKeyboardMarkup(keyboard))
    else:
        update.message.reply_text("Пожалуйста, подпишись на канал @eto_vse_ty и нажми /start снова.")

def button(update: Update, context: CallbackContext):
    query = update.callback_query
    data = query.data
    text = messages.get(data, "✨ Послание для тебя уже в пути...")
    query.answer(text=text, show_alert=True)

def main():
    updater = Updater(TOKEN)
    dp = updater.dispatcher
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CallbackQueryHandler(button))
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
