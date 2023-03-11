from telegram.ext import ApplicationBuilder, MessageHandler, CommandHandler, filters
from telegram.request import HTTPXRequest
from telegram import Bot
import importlib

from TOKENS import TEST_TOKEN

mods = ['caus']

bot = Bot(
    token = TEST_TOKEN,
    request=HTTPXRequest(http_version="1.1"),
    get_updates_request=HTTPXRequest(http_version="1.1"),
) # https://github.com/python-telegram-bot/python-telegram-bot/issues/3556
    
app = ApplicationBuilder().bot(bot).build()

for mod_name in mods:
    previewer = importlib.import_module(f"Previewers.{mod_name}")
    pattern = getattr(previewer, mod_name).pattern
    preview = getattr(previewer, mod_name).preview
    app.add_handler(MessageHandler(filters.Regex(pattern), preview))

app.run_polling()