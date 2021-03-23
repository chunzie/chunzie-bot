import os
import logging
from telegram import (
    Update,
    ReplyKeyboardMarkup,
    ReplyKeyboardRemove)
from telegram.ext import (
    Filters,
    MessageHandler,
    Updater,
    CommandHandler,
    ConversationHandler,
    CallbackContext)
from plexapi.server import PlexServer

### Telegram Variables ###
TOKEN = os.getenv('BOT_TOKEN')
WEBHOOK_URL = os.getenv('WEBHOOK_URL')

### Plex Variables ###
PLEX_URL = os.getenv('PLEX_URL')
PLEX_TOKEN = os.getenv('PLEX_TOKEN')
PLEX = None

if TOKEN is None \
        or WEBHOOK_URL is None \
        or PLEX_URL is None \
        or PLEX_TOKEN is None:
    print('Invalid configuration. Make sure all of the environment variables are set.')
    exit(1)

WHITELIST_PATH = '/config/whitelist'
whitelist = []
if os.path.exists(WHITELIST_PATH):
    with open(WHITELIST_PATH) as f:
        for line in f:
            whitelist.append(int(line.strip()))

if len(whitelist) == 0:
    print(
        'Invalid configuration. Make sure there is a whitelist attached to /config/whitelist with at least 1 chat ID.')
    exit(1)

# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)

logger = logging.getLogger(__name__)

# Conversation states
RUN_SCAN = 0


def scan(update: Update, context: CallbackContext) -> int:
    user = update.message.from_user
    logger.info(f'Scan prompt started by {user.username} from chat {update.effective_chat.id}')
    # Get the libraries
    libraries = PLEX.library.sections()
    titles = [library.title for library in libraries]

    # Present the prompt
    context.bot.send_message(chat_id=update.effective_chat.id,
                             text='Select the library you would like to scan or type /cancel to stop',
                             reply_markup=ReplyKeyboardMarkup.from_column(titles, one_time_keyboard=True))

    return RUN_SCAN


def run_scan(update: Update, _: CallbackContext) -> int:
    user = update.message.from_user
    library = update.message.text
    PLEX.library.section(library).update()
    logger.info(f'Scan started on "{library}" library  by {user.username} from chat {update.effective_chat.id}')
    update.message.reply_text(f'Scan started on {library} library...', reply_markup=ReplyKeyboardRemove())
    return ConversationHandler.END


def cancel(update: Update, _: CallbackContext) -> int:
    user = update.message.from_user
    logger.info(f'User {user.username} canceled the conversation in chat {update.effective_chat.id}')
    update.message.reply_text('Scan canceled.', reply_markup=ReplyKeyboardRemove())
    return ConversationHandler.END


def main() -> None:
    global PLEX
    PLEX = PlexServer(PLEX_URL, PLEX_TOKEN)

    updater = Updater(TOKEN)
    dispatcher = updater.dispatcher

    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('scan', scan, Filters.chat(whitelist))],
        states={
            RUN_SCAN: [CommandHandler('cancel', cancel), MessageHandler(Filters.update, run_scan)],
        },
        fallbacks=[CommandHandler('cancel', cancel)]
    )

    dispatcher.add_handler(conv_handler)

    updater.start_webhook(webhook_url=WEBHOOK_URL, listen='0.0.0.0')
    updater.idle()


if __name__ == '__main__':
    main()
