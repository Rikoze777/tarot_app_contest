from tarot.views import get_predicton, get_user
from django.urls import path

app_name = "tarot"

urlpatterns = [
    path('prediction', get_predicton, name='get_predicton'),
    path('user', get_user, name='get_user')
]
