from tarot.models import User, Subscription


def is_new_user(user_id):
    return not User.objects.filter(tg_id=user_id).exists()


def save_user_data(data):
    User.objects.create(tg_id=data["user_id"])


def validate_fullname(fullname):
    if len(fullname) > 1:
        return True


def delete_user(user_id):
    User.objects.filter(tg_id__contains=user_id).delete()


def get_user_role(user_id):
    return Subscription.objects.get(user__tg_id=user_id).role
