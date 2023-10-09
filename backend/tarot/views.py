from django.conf import settings
from rest_framework.decorators import api_view, authentication_classes
from rest_framework.response import Response
from telegram import Bot, LabeledPrice
from tarot.services.user_utils import get_invoice, get_user_sub
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
    user_id = request.user.tg_id
    sub = get_user_sub(user_id)
    context = {
        'tg_id': user_id,
        'level': sub.role
    }
    return Response(context)


@api_view(['POST'])
@authentication_classes([TelegramAuthentication])
def send_invoice(request, format=None):
    user = request.user
    bot = Bot(settings.BOT_API_TOKEN)
    invoice_link = bot.create_invoice_link(
        "Buy subscription",
        "Subscription for 1 month",
        get_invoice(user).uuid.hex,
        settings.PROVIDER_TOKEN,
        "RUB",
        [LabeledPrice("Monthly Subscription", 20000)]
    )
    resp = {
        "invoice_link" : invoice_link
    }
    return Response(resp)