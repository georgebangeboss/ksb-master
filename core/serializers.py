from rest_framework import serializers
from .models import DailyWorkSheet,FieldPhoto


class DailyWorkSheetSerializer(serializers.ModelSerializer):

    class Meta:
        model = DailyWorkSheet
        fields = '__all__'


class FieldPhoto(serializers.ModelSerializer):

    class Meta:
        model = FieldPhoto
        fields = '__all__'