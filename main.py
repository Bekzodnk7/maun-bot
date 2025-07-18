import sqlite3
from telegram import Update
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, ConversationHandler, CallbackContext

# ===== DATABASE =====
def init_db():
    conn = sqlite3.connect('maun.db')
    cursor = conn.cursor()

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS groups (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            group_id INTEGER,
            telegram_id INTEGER,
            name TEXT,
            is_admin BOOLEAN,
            FOREIGN KEY (group_id) REFERENCES groups(id)
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS items (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            group_id INTEGER,
            user_id INTEGER,
            name TEXT,
            category TEXT,
            expiry_date TEXT,
            is_taken BOOLEAN,
            taken_by INTEGER,
            FOREIGN KEY (group_id) REFERENCES groups(id),
            FOREIGN KEY (user_id) REFERENCES users(id)
        )
    ''')

    conn.commit()
    conn.close()

# ===== /add FUNCTION =====
ADD_NAME, ADD_CATEGORY, ADD_EXPIRY = range(3)

def start_add(update: Update, context: CallbackContext):
    update.message.reply_text("Қўшмоқчи бўлган буюминг номини ёзинг:")
    return ADD_NAME

def add_name(update: Update, context: CallbackContext):
    context.user_data['item_name'] = update.message.text
    update.message.reply_text("Категорияни ёзинг: асбоб-ускуна / техника / дори-дармон / китоб / рўзғор буюми")
    return ADD_CATEGORY

def add_category(update: Update, context: CallbackContext):
    category = update.message.text.lower()
    context.user_data['item_category'] = category
    if category == 'дори-дармон':
        update.message.reply_text("Яроқлилик муддатини киритинг (йил-ой-кун):")
        return ADD_EXPIRY
    else:
        save_item(update, context, expiry_date=None)
        update.message.reply_text("Буюм қўшилди ✅")
        return ConversationHandler.END

def add_expiry(update: Update, context: CallbackContext):
    expiry_date = update.message.text
    save_item(update, context, expiry_date)
    update.message.reply_text("Дори қўшилди ✅")
    return ConversationHandler.END

def save_item(update, context, expiry_date):
    user_id = update.effective_user.id
    group_id = 1  # Вақтинча тест учун. Кейин гуруҳ ID динамик қиламиз.

    conn = sqlite3.connect('maun.db')
    cursor = conn.cursor()

    cursor.execute('''
        INSERT INTO items (group_id, user_id, name, category, expiry_date, is_taken)
        VALUES (?, ?, ?, ?, ?, ?)
    ''', (group_id, user_id,
          context.user_data['item_name'],
          context.user_data['item_category'],
          expiry_date,
          False))
    conn.commit()
    conn.close()

# ===== TELEGRAM SETUP =====
def main():
    init_db()

    updater = Updater("SENING-TOKEN-ЁЗИЛАДИ", use_context=True)
    dispatcher = updater.dispatcher

    # /add HANDLER
    add_conv_handler = ConversationHandler(
        entry_points=[CommandHandler('add', start_add)],
        states={
            ADD_NAME: [MessageHandler(Filters.text & ~Filters.command, add_name)],
            ADD_CATEGORY: [MessageHandler(Filters.text & ~Filters.command, add_category)],
            ADD_EXPIRY: [MessageHandler(Filters.text & ~Filters.command, add_expiry)],
        },
        fallbacks=[]
    )
    dispatcher.add_handler(add_conv_handler)

    # /start
    dispatcher.add_handler(CommandHandler('start', lambda update, context: update.message.reply_text('Assalomu alaykum! Bu Ma\'un bot. /add билан буюм қўшинг.')))

    updater.start_polling()
    updater.idle()

# ===== RUN =====
if __name__ == '__main__':
    main()

