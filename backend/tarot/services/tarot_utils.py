from datetime import timedelta
import random
from django.utils import timezone
from tarot.models import Card, Prediction


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


def save_prediction(user_id, prediction):
    # prediction_list = ['day', 'love', 'yes_or_no', 'finance', 'advise']
    prediction = Prediction(
        user=user_id,
        date=timezone.now(),
        prediction=prediction,
    )
    prediction.save()


def check_user_prediction(user_id, prediction):
    end_date = timezone.now()
    start_date = end_date - timedelta(hours=24)
    try:
        checked = Prediction.objects.get(user=user_id,
                                         prediction=prediction,
                                         date__gte=start_date)
        context = {
            'user': checked.user,
            'date': checked.date,
            'prediction': checked.prediction
        }
        return context
    except Prediction.DoesNotExist:
        pred = Prediction(
            user=user_id,
            date=timezone.now(),
            prediction=prediction,
        )
        pred.save()
        context = {
            'user': pred.user,
            'date': pred.date,
            'prediction': pred.prediction
        }
        return context
