import json
from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from tarot.auth import parse_user_data, validate
from tarot.services.tarot_utils import (get_tarot_id, save_prediction,
                                        check_user_prediction, get_predn)
from django.core.exceptions import ValidationError
from environs import Env

env = Env()
env.read_env()


@csrf_exempt
@require_http_methods(['GET'])
def get_predicton(request):
    try:
        data_auth = request.META.get('Authorization')
        secret = env('TG_TOKEN')
        validate(data_auth, secret)
        data = parse_user_data(data_auth)
        number = get_tarot_id()
        predn = get_predn(number, data)
        context = check_user_prediction(data['user_id'], data['prediction'])
        context['prediction_disc'] = predn['prediction']
        return JsonResponse(data=context, status=200)
    except ValidationError as err:
        return JsonResponse({'message': str(err)}, status=400)
    except Exception as err:
        return JsonResponse({'message': 'An error occurred'}, status=500)
