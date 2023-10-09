from datetime import timedelta
import json
import random
from django.utils import timezone
from tarot.models import Card, Prediction, User


def get_tarot_id():
    return random.randint(1, 78)


def get_predn(number, prediction_type):
    card_queryset = Card.objects.get(id=number)
    card = card_queryset.card
    image = card_queryset.image.url
    if prediction_type == 'yes_or_no':
        prediction = card_queryset.yes_or_no
    elif prediction_type == 'advise':
        prediction = card_queryset.advise
    elif prediction_type == 'day':
        prediction = card_queryset.day
    elif prediction_type == 'love':
        prediction = card_queryset.love
    elif prediction_type == 'finance':
        prediction = card_queryset.finance
    context = {
        'card': card,
        'image': image,
        'prediction': prediction,
    }
    return context


def check_user_prediction(user_id, prediction_type):
    end_date = timezone.now()
    start_date = end_date - timedelta(days=1)
    user = User.objects.get(tg_id=user_id)
    try:
        checked = Prediction.objects.get(user__tg_id=user_id,
                                         prediction=prediction_type,
                                         date__gte=start_date)
        context = {
            'user': checked.user.tg_id,
            'prediction': checked.card.getDescription(prediction_type),
            'image': checked.card.image.url,
            'prediction_type': prediction_type
        }
        return context
    except Prediction.DoesNotExist:
        number = get_tarot_id()
        card = Card.objects.get(id=number)
        created = Prediction.objects.create(user=user,
                                            prediction=prediction_type,
                                            card=card,
                                            date=end_date)
        context = {
            'user': created.user.tg_id,
            'prediction': card.getDescription(prediction_type),
            'image': card.image.url,
            'prediction_type': prediction_type
        }
        return context
