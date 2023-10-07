from backend.tarot.views import get_predicton
from django.urls import path

app_name = "tarot"

urlpatterns = [
    path('', get_predicton, name='get_predicton'),
]
