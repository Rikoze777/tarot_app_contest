import requests
from rest_framework.decorators import api_view, authentication_classes
from rest_framework.response import Response
from telegram import LabeledPrice
from tarot.services.user_utils import get_user_sub, get_uuid
from tarot.serializers import UserSerializer
from tarot.auth import TelegramAuthentication
from tarot.services.tarot_utils import check_user_prediction
from django.conf import settings


@api_view(['GET'])
@authentication_classes([TelegramAuthentication])
def get_predicton(request, format=None):
    prediction_type = request.query_params.get('type')
    context = check_user_prediction(request.user.tg_id,
                                    prediction_type)
    return Response(context)


@api_view(['GET'])
@authentication_classes([TelegramAuthentication])
def get_user(request, format=None):
    user_data = UserSerializer(request.user).data
    sub = get_user_sub(user_data.get('tg_id'))
    context = {
        'tg_id': user_data['tg_id'],
        'sub': sub
    }
    return Response(context)


@api_view(['POST'])
@authentication_classes([TelegramAuthentication])
def send_invoice(request, format=None):
    user_id = request.user.tg_id
    bot_token = settings.BOT_API_TOKEN
    provider_token = settings.PROVIDER_TOKEN
    payload = get_uuid(user_id)
    data = {
        "title": "Buy subscription",
        "description": "Subscription for 1 month",
        "payload": payload,
        "provider_token": provider_token,
        "currency": "RUB",
        "prices": [LabeledPrice("Monthly Subscription", 20000)],
    }

    url = f'https://api.telegram.org/bot{bot_token}/createInvoiceLink'
    response = requests.post(url, data=data)
    return Response(response)
