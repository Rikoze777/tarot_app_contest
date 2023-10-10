from zodiac.settings import BOT_API_TOKEN
from tarot.models import User
from rest_framework import authentication
from rest_framework import exceptions
from tarot.utils import parse_init_data, parse_user_data, validate_init_data

class TelegramAuthentication(authentication.BaseAuthentication):
    def authenticate(self, request):
        init_data = request.META.get('HTTP_AUTHORIZATION')
        token = BOT_API_TOKEN
        if not init_data:
            raise exceptions.AuthenticationFailed('No valid authorization data provided')
        isValid = validate_init_data(init_data, token)
        if not isValid:
            raise exceptions.AuthenticationFailed('Authorization data not valid')
        init_data = parse_init_data(init_data)
        user_data = parse_user_data(init_data["user"])

        try:
            user = User.objects.get(tg_id=str(user_data["id"]))
        except User.DoesNotExist:
            raise exceptions.AuthenticationFailed('No such user')

        return (user, None)