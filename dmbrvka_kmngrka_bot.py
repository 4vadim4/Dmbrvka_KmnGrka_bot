# -*- coding: utf-8 -*-
import logging
from telegram.ext import Updater, MessageHandler, Filters
from config import token, user_id


logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)
logger = logging.getLogger(__name__)


def get_data(input_data):
    sender_id = input_data.chat.id
    username = '@' + input_data.chat.username if input_data.chat.username else 'no_username'
    first_name = input_data.chat.first_name if input_data.chat.first_name else 'no_firstname'
    last_name = input_data.chat.last_name if input_data.chat.last_name else 'no_lastname'
    return sender_id, username, first_name, last_name


def send_text(update, context):
    sender_id, username, first_name, last_name = get_data(update.message)

    context.bot.send_message(chat_id=user_id, text=update.message.text)
    logger.info('%s: (%s - %s %s) leave a message' % (sender_id, username, first_name, last_name))
    update.message.reply_text('Ваше сообщение отправлено нашим Администраторам!\nСпасибо!')


def send_photo(update, context):
    sender_id, username, first_name, last_name = get_data(update.message)
    description = update.message.caption if update.message.caption else ''

    context.bot.send_photo(chat_id=sender_id, photo=update.message.photo[0].file_id,
                           caption=description if description else None)
    logger.info('%s: (%s - %s %s) leave a photo' % (sender_id, username, first_name, last_name))

    update.message.reply_text('Ваше фото отправлено нашим Администраторам!\nСпасибо!')


def send_video(update, context):
    sender_id, username, first_name, last_name = get_data(update.message)
    description = update.message.caption if update.message.caption else ''

    context.bot.send_video(chat_id=sender_id, video=update.message.video.file_id,
                           caption=description if description else None)
    logger.info('%s: (%s - %s %s) leave a video' % (sender_id, username, first_name, last_name))

    update.message.reply_text('Ваше видео отправлено нашим Администраторам!\nСпасибо!')


def main():
    updater = Updater(token, use_context=True)
    dp = updater.dispatcher
    dp.add_handler(MessageHandler(Filters.photo, send_photo))
    dp.add_handler(MessageHandler(Filters.video, send_video))
    dp.add_handler(MessageHandler(Filters.text, send_text))
    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()
