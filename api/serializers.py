from rest_framework import serializers
from .models import ImageModel


class ImageModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = ImageModel
        fields = ('id', 'image', 'description', 'prediction_result')
        read_only_fields = ('prediction_result', 'description',)
