from image_handler.models import ImageModel
from rest_framework import serializers

class ImageSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = ImageModel
        fields = [
            'id',
            'file',
            ]
