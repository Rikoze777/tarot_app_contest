
# import datetime
import logging
from enum import Enum, auto

from telegram import (
    LabeledPrice,
    Update,
)
from telegram.ext import (
    Updater,
    CommandHandler,
    CallbackContext,

)
from django.core.management.base import BaseCommand
from django.conf import settings
# from django.utils import timezone

from tarot.models import Invoice
from tarot.services.user_utils import (
    is_new_user,
    save_user_data,
)


logger = logging.getLogger(__name__)


class States(Enum):
    start = auto()
    check_invoice = auto()


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

        dispatcher.add_handler(CommandHandler('start', start))

        updater.run_polling()
        updater.idle()


def start(update: Update, context: CallbackContext) -> int:
    user_id = update.effective_user.id
    chat_id = update.effective_chat.id
    if is_new_user(user_id):
        save_user_data(user_id)
    context.bot.send_message(
        chat_id=chat_id,
        text="Hello!",
        parse_mode="Markdown"
    )
    payload, created = Invoice.objects.get_or_create(user__tg_id=user_id)
    context.bot.send_invoice(
        chat_id=chat_id,
        title="Buy subscription",
        description="Subscription for 1 month",
        payload=str(payload),
        provider_token='381764678:TEST:68433',
        currency="RUB",
        prices=[LabeledPrice("Monthly Subscription", 20000)],
    )
    return States.check_invoice

