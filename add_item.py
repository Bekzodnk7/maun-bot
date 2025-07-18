from flask import request
import sqlite3
from telegram import Bot, Update
from telegram.ext import CommandHandler, MessageHandler, Filters, ConversationHandler

ADD_NAME, ADD_CATEGORY, ADD_EXPIRY = range(3)

def start_add(update, context):
    update.message.reply_text("Қўшмоқчи бўлган буюминг номини ёзинг:")
    return ADD_NAME

def add_name(update, context):
    context.user_data['item_name'] = update.message.text
    update.message.reply_text("Категорияни танланг: асбоб-ускуна / техника / дори-дармон / китоб / рўзғор буюми")
    return ADD_CATEGORY

def add_category(update, context):
    category = update.message.text
    context.user_data['item_category'] = category.lower()

    if category.lower() == 'дори-дармон':
        update.message.reply_text("Яроқлилик муддатини киритинг (йил-ой-кун):")
        return ADD_EXPIRY
    else:
        save_item(update, context, expiry_date=None)
        update.message.reply_text("Буюм қўшилди.")
        return ConversationHandler.END

def add_expiry(update, context):
    expiry_date = update.message.text
    save_item(update, context, expiry_date)
    update.message.reply_text("Дори қўшилди.")
    return ConversationHandler.END

def save_item(update, context, expiry_date):
    user_id = update.effective_user.id
    group_id = 1  # Вақтинча тест учун. Кейин гуруҳ ID динамик бўлади.

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

# Conversation handler
add_conv_handler = ConversationHandler(
    entry_points=[CommandHandler('add', start_add)],
    states={
        ADD_NAME: [MessageHandler(Filters.text & ~Filters.command, add_name)],
        ADD_CATEGORY: [MessageHandler(Filters.text & ~Filters.command, add_category)],
        ADD_EXPIRY: [MessageHandler(Filters.text & ~Filters.command, add_expiry)],
    },
    fallbacks=[]
)
