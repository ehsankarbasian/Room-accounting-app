from rest_framework.serializers import ModelSerializer, ValidationError

from .models import Token


class TokenSerializer(ModelSerializer):
    class Meta:
        model = Token
        fields = '__all__'
