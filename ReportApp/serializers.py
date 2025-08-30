from rest_framework.serializers import ModelSerializer, ValidationError

from ReportApp.models import Token


class TokenSerializer(ModelSerializer):
    class Meta:
        model = Token
        fields = '__all__'
