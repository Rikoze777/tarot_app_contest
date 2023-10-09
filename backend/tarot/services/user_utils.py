from tarot.models import Invoice, User, Subscription


def is_new_user(user_id):
    return not User.objects.filter(tg_id=str(user_id)).exists()


def save_user_data(user_id):
    User.objects.create(tg_id=str(user_id))


def validate_fullname(fullname):
    if len(fullname) > 1:
        return True


def delete_user(user_id):
    User.objects.filter(tg_id__contains=user_id).delete()


def get_user_sub(user_id):
    return Subscription.objects.get(user__tg_id=user_id)


def get_invoice(user):
    payload, created = Invoice.objects.get_or_create(user=user)
    return payload
