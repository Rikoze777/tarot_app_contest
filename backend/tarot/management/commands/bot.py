import datetime
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
from django.utils import timezone

from tarot.models import User, Card, Prediction, Subscription
from backend.tarot.services.user_utils import (
    is_new_user,
    save_user_data,
    get_user_sub,
    delete_user
)

logger = logging.getLogger(__name__)


class States(Enum):
    start = auto()
    authorization = auto()
    save_us = auto()
    choose_role = auto()
    user = auto()
    level1 = auto()


class Transitions(Enum):
    authorization_reject = auto()
    authorization_approve = auto()
    user = auto()
    level1 = auto()
    speaker_events = auto()
    create_event = auto()
    event = auto()


class Command(BaseCommand):
    help = 'Implemented to Django application telegram bot setup command'

    def handle(self, *args, **kwargs):
        updater = Updater(token=settings.TG_BOT_TOKEN)

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
                        MessageHandler(Filters.text, get_data),
                    ],
                States.save_us:
                    [
                        MessageHandler(Filters.text, save_user),
                        MessageHandler(Filters.contact, save_user),
                    ],
                # States.choose_role:
                #     [
                #         CallbackQueryHandler(handle_role),
                #     ],
                # States.user:
                #     [
                #         CallbackQueryHandler(show_events, pattern=f'^{Transitions.events}$'),
                #         # CallbackQueryHandler(choose_event, pattern=f'^{Transitions.event}$'),
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
        return States.choose_role


def callback_approve_handler(update: Update, context: CallbackContext) -> int:
    chat_id = update.effective_chat.id
    query = update.callback_query
    data = query.data

    # if data == str(Transitions.authorization_approve):
    #     context.bot.send_message(
    #         chat_id=chat_id,
    #         text="Сначала введите имя, после фамилию"
    #     )
    #     return States.authorization
    if data == str(Transitions.authorization_reject):
        context.bot.send_message(
            chat_id=chat_id,
            text="Without a processing agreement, we cannot provide you with a service."
        )
        return ConversationHandler.END


def handle_role(update: Update, context: CallbackContext) -> int:
    chat_id = update.effective_chat.id
    user_role = get_user_sub(chat_id)
    query = update.callback_query
    query.answer()
    data = query.data
    if data == str(Transitions.user):
        keyboard = [
            [InlineKeyboardButton("Events", callback_data=str(Transitions.events))],
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        query.message.reply_text(
            text="Куда отправимся?",
            reply_markup=reply_markup,
        )
        return States.user
    elif data == str(Transitions.speaker):
        if user_role == "S":
            keyboard = [
                [InlineKeyboardButton("События", callback_data=str(Transitions.events))],
                [InlineKeyboardButton("Мои события", callback_data=str(Transitions.speaker_events))],
            ]
            reply_markup = InlineKeyboardMarkup(keyboard)
            query.message.reply_text(
                text="Выберете меню",
                reply_markup=reply_markup,
            )
            return States.speaker
        else:
            message = "К сожалению вы не докладчик"
    elif data == str(Transitions.organizer):
        if user_role == "O":
            keyboard = [
                [InlineKeyboardButton("Мои события", callback_data=str(Transitions.events))],
                [InlineKeyboardButton("Создать событие", callback_data=str(Transitions.create_event))],
            ]
            reply_markup = InlineKeyboardMarkup(keyboard)
            query.message.reply_text(
                text="Выберете меню",
                reply_markup=reply_markup,
            )
            return States.organizer
        else:
            message = "К сожалению, вы не организатор"
    keyboard = [
        [InlineKeyboardButton("Пользователь", callback_data=str(Transitions.user))],
        [InlineKeyboardButton("Докладчик", callback_data=str(Transitions.speaker))],
        [InlineKeyboardButton("Организатор", callback_data=str(Transitions.organizer))],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    query.message.reply_text(
        text=message,
        reply_markup=reply_markup,
    )
    return States.choose_role


def get_data(update: Update, context: CallbackContext) -> int:
    user_name = update.message.text
    context.user_data["user_id"] = update.message.from_user.id
    context.user_data["full_name"] = user_name
    return States.save_us


def save_user(update: Update, context: CallbackContext) -> int:
    chat_id = update.effective_chat.id

    if is_new_user(context.user_data["user_id"]):
        save_user_data(context.user_data)

    context.bot.send_message(
        chat_id=chat_id,
        text="*Вы прошли регистрацию*",
        parse_mode="Markdown"
    )
    keyboard = [
            [InlineKeyboardButton("Пользователь", callback_data=str(Transitions.user))],
            [InlineKeyboardButton("Докладчик", callback_data=str(Transitions.speaker))],
            [InlineKeyboardButton("Организатор", callback_data=str(Transitions.organizer))],
        ]
    context.bot.send_message(
        chat_id=chat_id,
        text="Пользователь-просмотр событий\nДокладчик-участие в событие\nОрганизатор-создание события",
        reply_markup=InlineKeyboardMarkup(keyboard),
        parse_mode="Markdown"
    )
    return States.choose_role


###############################  USER #################################################################
def show_events(update: Update, context: CallbackContext) -> int:
    chat_id = update.effective_chat.id
    user_role = get_user_sub(chat_id)
    query = update.callback_query
    query.answer()
    data = query.data
    keyboard = []
    if user_role=='U':
        for event in events:
            keyboard.append([InlineKeyboardButton(f'{event.name}', callback_data=str(Transitions.events))])
    else:
        context.bot.send_message(
            chat_id=chat_id,
            text="Простите, но события отсутствуют",
            parse_mode="Markdown"
        )
    keyboard.append([InlineKeyboardButton('Назад', callback_data=str(Transitions.user))])
    reply_markup = InlineKeyboardMarkup(keyboard)
    query.message.reply_text(
        text="События",
        reply_markup=reply_markup,
    )
    return States.user

#######################################################################################################

def cancel(update: Update, context: CallbackContext) -> int:
    update.message.reply_text(
        'Надеюсь тебе понравился наш бот!'
    )

    return ConversationHandler.END
