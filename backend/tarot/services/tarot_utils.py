from datetime import timedelta
import random
from django.utils import timezone
from backend.tarot.models import Prediction


def get_tarot_id():
    tarot_numbers = list(range(1, 79))
    random.shuffle(tarot_numbers)
    choosen_number = random.choice[tarot_numbers]

    return choosen_number


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
    except Prediction.DoesNotExist:
        return True
    return False
