from rest_framework import serializers

from tarot.models import User

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['tg_id']