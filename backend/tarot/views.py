from rest_framework.decorators import api_view, authentication_classes
from rest_framework.response import Response
from tarot.serializers import UserSerializer
from tarot.auth import TelegramAuthentication

from tarot.services.tarot_utils import (get_tarot_id, save_prediction,
                                        check_user_prediction, get_predn)


@api_view(['GET'])
@authentication_classes([TelegramAuthentication])
def get_predicton(request, format=None):
    prediction_type = request.query_params.get('type')
    number = get_tarot_id()
    predn = get_predn(number, prediction_type)
    context = check_user_prediction(request.user.tg_id, prediction_type)
    context['prediction_disc'] = predn['prediction']
    return Response(context)
    
@api_view(['GET'])
@authentication_classes([TelegramAuthentication])
def get_user(request, format=None):
    user_data = UserSerializer(request.user).data
    return Response(user_data)