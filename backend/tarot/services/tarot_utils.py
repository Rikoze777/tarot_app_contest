from datetime import timedelta
import random
from django.utils import timezone
from tarot.models import Card, Prediction, User


def get_tarot_id():
    return random.randint(1, 78)

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
