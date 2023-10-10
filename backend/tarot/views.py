from django.conf import settings
from rest_framework.decorators import api_view, authentication_classes
from rest_framework.response import Response
from telegram import Bot
from tarot.services.user_utils import create_invoice, get_actual_subscription, get_invoice_params
from tarot.auth import TelegramAuthentication
from tarot.services.tarot_utils import check_user_prediction
from django.conf import settings
from asgiref.sync import async_to_sync


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
    user = request.user
    sub = get_actual_subscription(user)
    context = {
        'id': user.id,
        'subscribed': sub is not None
    }
    return Response(context)


@api_view(['POST'])
@authentication_classes([TelegramAuthentication])
def send_invoice(request, format=None):
    invoice = create_invoice(request.user)
    params = get_invoice_params(invoice)
    bot = Bot(settings.BOT_API_TOKEN)
    invoice_link = async_to_sync(
        bot.create_invoice_link
    )(params['title'],
      params['description'],
      params['payload'],
      settings.PROVIDER_TOKEN,
      params['currency'],
      params['prices'])
    resp = {
        "invoice_link": invoice_link
    }
    return Response(resp)
