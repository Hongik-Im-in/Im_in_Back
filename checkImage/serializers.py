from rest_framework import serializers
from django.core.files import File
import base64
from checkImage.models import checkImage

class CheckSerializer(serializers.ModelSerializer):
    image = serializers.ImageField(use_url=True)

    class Meta:
        model = checkImage
        fields = ['title', 'image']


    def create(self, validated_data):
        return checkImage.objects.create(**validated_data)

    def update(self, instance, validated_data):
        """
        Update and return an existing `Snippet` instance, given the validated data.
        """
        instance.title = validated_data.get('title', instance.title)
        instance.image = validated_data.get('image', instance.image)

        instance.save()
        return instance

