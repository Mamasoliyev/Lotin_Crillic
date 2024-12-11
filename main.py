import logging
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, CallbackContext
from dotenv import load_dotenv
import os
import re

# Load environment variables from .env file
load_dotenv()

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)
logger = logging.getLogger(__name__)

# Helper functions
def is_latin(text):
    """Tekshiradi: Matn faqat lotin harflaridan tashkil topganmi."""
    return bool(re.match(r'^[a-zA-Z\'\s]*$', text))

def latin_to_cyrillic(text):
    if not is_latin(text):  # Agar matn lotin alifbosida bo‘lmasa, hech narsa qilmang
        return None  # Javob qaytarmaslik uchun
    translit_map_upper = [
        ("G'", 'Ғ'), ('Ts', 'Ц'), ('Yo', 'Ё'), ("O'", 'Ў'), ('Ch', 'Ч'), ('Sh', 'Ш'), ('Yu', 'Ю'), ('Ya', 'Я'),
        ('Ye', 'Е'), ('A', 'А'), ('B', 'Б'), ('V', 'В'), ('G', 'Г'), ('D', 'Д'),
        ('E', 'Э'), ('F', 'Ф'), ('H', 'Х'), ('I', 'И'), ('J', 'Ж'), ('K', 'К'),
        ('L', 'Л'), ('M', 'М'), ('N', 'Н'), ('O', 'О'), ('P', 'П'), ('Q', 'Қ'),
        ('R', 'Р'), ('S', 'С'), ('T', 'Т'), ('U', 'У'), ('V', 'В'), ('W', 'W'),
        ('X', 'X'), ('Y', 'Й'), ('Z', 'З'), ('W', 'Ш')
    ]

    translit_map_lower = [
        ("g'", 'ғ'), ('ts', 'ц'), ('yo', 'ё'), ("o'", 'ў'), ('ch', 'ч'), ('sh', 'ш'), ('yu', 'ю'), ('ya', 'я'),
        ('ye', 'е'), ('a', 'а'), ('b', 'б'), ('v', 'в'), ('g', 'г'), ('d', 'д'),
        ('e', 'э'), ('f', 'ф'), ('h', 'х'), ('i', 'и'), ('j', 'ж'), ('k', 'к'),
        ('l', 'л'), ('m', 'м'), ('n', 'н'), ('o', 'о'), ('p', 'п'), ('q', 'қ'),
        ('r', 'р'), ('s', 'с'), ('t', 'т'), ('u', 'у'), ('v', 'в'), ('w', 'w'),
        ('x', 'x'), ('y', 'й'), ('z', 'з'), ('w', 'ш')
    ]

    # Katta harflar uchun almashirish
    for latin, cyrillic in translit_map_upper:
        text = text.replace(latin, cyrillic)

    # Kichik harflar uchun almashirish
    for latin, cyrillic in translit_map_lower:
        text = text.replace(latin, cyrillic)

    return text

# Command handlers
async def start(update: Update, context: CallbackContext) -> None:
    await update.message.reply_text('Assalomu alaykum! Lotincha matn yuboring, men uni kirilchaga o‘girib beraman.')

async def convert_to_cyrillic(update: Update, context: CallbackContext) -> None:
    text = update.message.text
    if text.startswith('/'):  # Komandalarni o'tkazib yuborish
        return
    converted_text = latin_to_cyrillic(text)
    if converted_text:  # Agar javob bo'lsa, uni qaytarish
        await update.message.reply_text(converted_text)

def main():
    # Read the token from the environment variable
    api_token = os.getenv("BOT_API_TOKEN")

    # Check if the token is available
    if api_token is None:
        print("Error: BOT_API_TOKEN not set in the environment variables.")
        return

    # Initialize the application with the API token
    application = Application.builder().token(api_token).build()

    # Register command and message handlers
    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, convert_to_cyrillic))

    # Start the bot
    application.run_polling()

if __name__ == '__main__':
    main()
