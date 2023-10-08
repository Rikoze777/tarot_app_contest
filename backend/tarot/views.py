from rest_framework.decorators import api_view, authentication_classes
from rest_framework.response import Response
from tarot.services.user_utils import get_user_sub
from tarot.serializers import UserSerializer
from tarot.auth import TelegramAuthentication

from tarot.services.tarot_utils import (get_tarot_id,
                                        check_user_prediction)


@api_view(['GET'])
@authentication_classes([TelegramAuthentication])
def get_predicton(request, format=None):
    prediction_type = request.query_params.get('type')
    number = get_tarot_id()
    context = check_user_prediction(request.user.tg_id,
                                    prediction_type, number)
    return Response(context)


@api_view(['GET'])
@authentication_classes([TelegramAuthentication])
def get_user(request, format=None):
    user_data = UserSerializer(request.user).data
    sub = get_user_sub(user_data)
    context = {
        'tg_id': user_data,
        'sub': sub
    }
    return Response(context)
