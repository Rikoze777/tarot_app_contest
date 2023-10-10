import logging
import os
from django.conf import settings
from telegram import Update
from telegram.ext import (
    Application,
    CommandHandler,
    ContextTypes,
    MessageHandler,
    PreCheckoutQueryHandler,
    filters,
)
from django.core.management.base import BaseCommand
from tarot.services.user_utils import create_invoice, create_subscription, delete_invoice, get_actual_subscription, get_invoice, get_invoice_params, get_user, is_new_user, save_user_data

logger = logging.getLogger(__name__)


async def start_callback(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Displays info on how to use the bot."""
    user_id = update.effective_user.id
    if is_new_user(user_id):
        save_user_data(user_id)
    username = update.effective_user.name
    msg = (
        f"Hello, {username}. Welcome to Tarot Bot. You can get daily predictions or advices on any questions."
        "All interactive functionality available through the 'Menu' button."
        "Use /subscribe to subscribe for a month and unlock Love, Finance, Question, Yes or No menu options."
    )

    await update.message.reply_text(msg)


async def precheckout_callback(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Answers the PreQecheckoutQuery"""
    user = get_user(update.effective_user.id)
    query = update.pre_checkout_query
    # check the payload, is this from your bot?
    exists = get_invoice(user, query.invoice_payload) is not None
    if exists:
        await query.answer(ok=True)
    else:
        # answer False pre_checkout_query
        await query.answer(ok=False, error_message="Something went wrong...")


async def subscribe_callback(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Sends an invoice for monthly subscription."""
    chat_id = update.message.chat_id
    user = get_user(update.effective_user.id)
    invoice = create_invoice(user)
    params = get_invoice_params(invoice)

    await context.bot.send_invoice(
        chat_id,
        params['title'],
        params['description'],
        params['payload'],
        settings.PROVIDER_TOKEN,
        params['currency'],
        params['prices'],
    )


async def subscription_check(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Checks current subscription."""
    user = get_user(update.effective_user.id)
    subscription = get_actual_subscription(user)
    if subscription is not None:
        start_date = subscription.date_from.strftime('%d %B, %Y')
        end_date = subscription.date_end.strftime('%d %B, %Y')
        await update.message.reply_text(
            f"Your subscription is valid from {start_date} to {end_date}"
        )
    else:
        await update.message.reply_text("You haven't subscribed yet")


async def successful_payment_callback(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Confirms the successful payment."""
    user = get_user(update.effective_user.id)
    payload = update.message.successful_payment.invoice_payload
    delete_invoice(user, payload)
    subscription = create_subscription(user)
    end_date = subscription.date_end.strftime('%d %B, %Y')
    await update.message.reply_text(f"Thank you for your payment! You have subscribed before {end_date}")


class Command(BaseCommand):
    help = 'Implemented to Django application telegram bot setup command'

    def handle(self, *args, **kwargs):
        """Run the bot."""
        os.environ["DJANGO_ALLOW_ASYNC_UNSAFE"] = "true"
        # Create the Application and pass it your bot's token.
        application = Application.builder().token(settings.BOT_API_TOKEN).build()

        # simple start function
        application.add_handler(CommandHandler("start", start_callback))

        # Add command handler to start the payment invoice
        application.add_handler(CommandHandler("subscribe", subscribe_callback))

        # Add command handler to start the payment invoice
        application.add_handler(CommandHandler("subscription", subscription_check))

        # Pre-checkout handler to final check
        application.add_handler(PreCheckoutQueryHandler(precheckout_callback))

        # Success! Notify your user!
        application.add_handler(
            MessageHandler(filters.SUCCESSFUL_PAYMENT, successful_payment_callback)
        )

        # Run the bot until the user presses Ctrl-C
        application.run_polling(allowed_updates=Update.ALL_TYPES)
