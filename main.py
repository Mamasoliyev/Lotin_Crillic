import re
import logging
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, CallbackContext
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

# Define the Latin-to-Cyrillic transliteration map
def latin_to_cyrillic(text):
    translit_map_upper = [
        ("G'", 'Ғ'), ('Ts', 'Ц'), ('Yo', 'Ё'), ('Ch', 'Ч'), ('Sh', 'Ш'), ('Yu', 'Ю'), ('Ya', 'Я'),
        ('Ye', 'Е'), ('A', 'А'), ('B', 'Б'), ('V', 'В'), ('G', 'Г'), ('D', 'Д'),
        ('E', 'Э'), ('F', 'Ф'), ('H', 'Х'), ('I', 'И'), ('J', 'Ж'), ('K', 'К'),
        ('L', 'Л'), ('M', 'М'), ('N', 'Н'), ('O', 'О'), ('P', 'П'), ('Q', 'Қ'),
        ('R', 'Р'), ('S', 'С'), ('T', 'Т'), ('U', 'У'), ('V', 'В'), ('W', 'W'),
        ('X', 'X'), ('Y', 'Й'), ('Z', 'З')
    ]

    translit_map_lower = [
        ("g'", 'ғ'), ('ts', 'ц'), ('yo', 'ё'), ('ch', 'ч'), ('sh', 'ш'), ('yu', 'ю'), ('ya', 'я'),
        ('ye', 'е'), ('a', 'а'), ('b', 'б'), ('v', 'в'), ('g', 'г'), ('d', 'д'),
        ('e', 'э'), ('f', 'ф'), ('h', 'х'), ('i', 'и'), ('j', 'ж'), ('k', 'к'),
        ('l', 'л'), ('m', 'м'), ('n', 'н'), ('o', 'о'), ('p', 'п'), ('q', 'қ'),
        ('r', 'р'), ('s', 'с'), ('t', 'т'), ('u', 'у'), ('v', 'в'), ('w', 'w'),
        ('x', 'x'), ('y', 'й'), ('z', 'з')
    ]

    for latin, cyrillic in translit_map_upper:
        text = text.replace(latin, cyrillic)

    for latin, cyrillic in translit_map_lower:
        text = text.replace(latin, cyrillic)

    return text

# Define command handlers
async def start(update: Update, context: CallbackContext) -> None:
    await update.message.reply_text('Hello! Send me any Latin text and I will convert it to Cyrillic.')

async def help_command(update: Update, context: CallbackContext) -> None:
    await update.message.reply_text('Send any text written in Latin characters, and I will convert it to Cyrillic.')

async def convert_to_cyrillic(update: Update, context: CallbackContext) -> None:
    # Check if the message is older and ignore it
    if update.message.date and (update.message.date < context.application.start_time):
        return

    text = update.message.text
    if not text.startswith('/') and re.search(r'[A-Za-z]', text):  # Only process if text has Latin characters
        converted_text = latin_to_cyrillic(text)
        await update.message.reply_text(converted_text)

def main():
    api_token = os.getenv("BOT_API_TOKEN")

    if api_token is None:
        print("Error: BOT_API_TOKEN not set in the environment variables.")
        return

    application = Application.builder().token(api_token).build()

    # Register command and message handlers
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, convert_to_cyrillic))

    application.run_polling()

if __name__ == '__main__':
    main()
