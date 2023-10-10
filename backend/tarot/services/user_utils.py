from datetime import timedelta
import uuid
from telegram import LabeledPrice
from tarot.models import Invoice, User, Subscription
from django.utils import timezone


def is_new_user(user_id):
    return not User.objects.filter(tg_id=str(user_id)).exists()


def save_user_data(user_id):
    User.objects.create(tg_id=str(user_id))


def validate_fullname(fullname):
    if len(fullname) > 1:
        return True


def get_user(user_id):
    return User.objects.get(tg_id=user_id)


def delete_user(user_id):
    User.objects.filter(tg_id__contains=user_id).delete()


def get_actual_subscription(user: User) -> Subscription | None:
    current_time = timezone.now()
    return Subscription.objects.filter(
        user=user,
        date_from__lte=current_time,
        date_end__gte=current_time
    ).first()


def create_subscription(user: User) -> Subscription:
    date_from = timezone.now()
    actual = get_actual_subscription(user)
    if actual is not None:
        actual.date_end = actual.date_end + timedelta(days=30)
        actual.save()
        return actual
    date_end = date_from + timedelta(days=30)
    return Subscription.objects.create(user=user, date_from=date_from, date_end=date_end)


def create_invoice(user: User) -> Invoice:
    invoice = Invoice.objects.create(user=user)
    return invoice


def get_invoice(user: User, invoice_id) -> Invoice | None:
    try:
        return Invoice.objects.get(user=user, uuid=uuid.UUID(invoice_id))
    except Invoice.DoesNotExist:
        return None


def delete_invoice(user: User, invoice_id: str) -> bool:
    invoice = get_invoice(user, invoice_id)
    if invoice is not None:
        invoice.delete()
        return True
    else:
        return False


def get_invoice_params(invoice: Invoice):
    title = "Your Premium subscription"
    description = "Access to Premium features for 1 month"
    payload = invoice.uuid.hex
    currency = "RUB"
    price = 200
    # price * 100 so as to include 2 decimal points
    # check https://core.telegram.org/bots/payments#supported-currencies for more details
    prices = [LabeledPrice("Monthly Subscription", price * 100)]
    return {
        'title': title,
        'description': description,
        'payload': payload,
        'currency': currency,
        'prices': prices
    }
