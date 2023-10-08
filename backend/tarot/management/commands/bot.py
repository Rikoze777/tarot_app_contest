
# import datetime
import logging
from enum import Enum, auto

from telegram import (
    KeyboardButton,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    ReplyKeyboardMarkup,
    Update,
)
from telegram.ext import (
    Updater,
    CommandHandler,
    MessageHandler,
    Filters,
    ConversationHandler,
    CallbackContext,
    CallbackQueryHandler,
)
from django.core.management.base import BaseCommand
from django.conf import settings
# from django.utils import timezone

# from tarot.models import User, Card, Prediction, Subscription
from tarot.services.user_utils import (
    is_new_user,
    save_user_data,
    get_user_sub,
)


logger = logging.getLogger(__name__)


class States(Enum):
    start = auto()
    authorization = auto()
    save_us = auto()
    choose_sub = auto()
    user = auto()
    level1 = auto()


class Transitions(Enum):
    authorization_reject = auto()
    authorization_approve = auto()
    subs = auto()
    get_sub = auto()
    renew = auto()
    current = auto()
    user = auto()
    level1 = auto()


class Command(BaseCommand):
    help = 'Implemented to Django application telegram bot setup command'

    def handle(self, *args, **kwargs):
        updater = Updater(token=settings.BOT_API_TOKEN)

        dispatcher = updater.dispatcher

        conv_handler = ConversationHandler(
            entry_points=[
                CommandHandler('start', start),
            ],
            states={
                States.authorization:
                    [
                        CallbackQueryHandler(
                            callback=callback_approve_handler,
                            pass_chat_data=True
                        ),
                    ],
                States.save_us:
                    [
                        MessageHandler(Filters.text, save_user),
                    ],
                States.choose_sub:
                    [
                        CallbackQueryHandler(handle_role, pattern=f'^{Transitions.subs}$'),
                    ],
                States.user:
                    [
                        CallbackQueryHandler(buy_subscription, pattern=f'^{Transitions.get_sub}$'),
                    ],
                # States.level1:
                #     [
                #         CallbackQueryHandler(buy_subscription, pattern=f'^{Transitions.get_sub}$'),
                #     ],
            },
            fallbacks=[
                CommandHandler('cancel', cancel),
                CommandHandler('start', cancel),
            ],
        )

        dispatcher.add_handler(conv_handler)

        updater.start_polling()
        updater.idle()


def start(update: Update, context: CallbackContext) -> int:
    user_id = update.effective_user.id
    if is_new_user(user_id):
        with open("Agreement.pdf", "rb") as image:
            agreement = image.read()

        keyboard = [
            [InlineKeyboardButton("Accept", callback_data=str(Transitions.authorization_approve))],
            [InlineKeyboardButton("Refuse", callback_data=str(Transitions.authorization_reject))],
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)

        update.message.reply_document(
            agreement,
            filename="Agreement.pdf",
            caption="To use the service, accept the agreement on the processing of personal data",
            reply_markup=reply_markup,
            parse_mode="Markdown"
        )
        return States.authorization
    else:
        role = get_user_sub(user_id)
        context.bot.send_message(
            chat_id=user_id,
            text=f"We are glad to see you again. Your subscription level is {role}"
        )
        return States.choose_sub


def callback_approve_handler(update: Update, context: CallbackContext) -> int:
    chat_id = update.effective_chat.id
    query = update.callback_query
    data = query.data
    if data == str(Transitions.authorization_approve):
        context.bot.send_message(
            chat_id=chat_id,
            text="Welcome!"
        )
        return States.save_us
    if data == str(Transitions.authorization_reject):
        context.bot.send_message(
            chat_id=chat_id,
            text="Without a processing agreement, we cannot provide you with a service."
        )
        return ConversationHandler.END


def save_user(update: Update, context: CallbackContext) -> int:
    chat_id = update.effective_chat.id
    if is_new_user(context.user_data["tg_id"]):
        save_user_data(context.user_data)
    context.bot.send_message(
        chat_id=chat_id,
        text="You are registered!",
        parse_mode="Markdown"
    )
    keyboard = [
            [InlineKeyboardButton("Subscriptions", callback_data=str(Transitions.subs))],
        ]
    context.bot.send_message(
        chat_id=chat_id,
        text="Мiew subscriptions",
        reply_markup=InlineKeyboardMarkup(keyboard),
        parse_mode="Markdown"
    )
    return States.choose_sub


def handle_role(update: Update, context: CallbackContext) -> int:
    chat_id = update.effective_chat.id
    user_role = get_user_sub(chat_id)
    query = update.callback_query
    query.answer()
    data = query.data
    if data == str(Transitions.user):
        keyboard = [
            [InlineKeyboardButton("Get subscription", callback_data=str(Transitions.get_sub))],
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        query.message.reply_text(
            text="Upgrade your subscription to 'magic'. All tarot layouts will be available to you",
            reply_markup=reply_markup,
        )
        return States.user
    elif data == str(Transitions.level1):
        if user_role == "L1":
            keyboard = [
                [InlineKeyboardButton("Renew your subscription", callback_data=str(Transitions.renew))],
                [InlineKeyboardButton("Current subscription", callback_data=str(Transitions.current))],
            ]
            reply_markup = InlineKeyboardMarkup(keyboard)
            query.message.reply_text(
                text="Information about your subscription",
                reply_markup=reply_markup,
            )
            return States.level1
        else:
            message = "К сожалению вы не докладчик"
    keyboard = [
        [InlineKeyboardButton("Пользователь", callback_data=str(Transitions.user))],
        [InlineKeyboardButton("Докладчик", callback_data=str(Transitions.level1))],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    query.message.reply_text(
        text=message,
        reply_markup=reply_markup,
    )
    return States.choose_sub


def buy_subscription(update: Update, context: CallbackContext)-> int:
    pass


def cancel(update: Update, context: CallbackContext) -> int:
    update.message.reply_text(
        'Надеюсь тебе понравился наш бот!'
    )

    return ConversationHandler.END
