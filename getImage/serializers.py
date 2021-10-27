from rest_framework import serializers
from django.core.files import File
import base64
from getImage.models import Check
from getImage.models import Images 


class ImageSerializer(serializers.ModelSerializer):
    image = serializers.ImageField(use_url=True)

    class Meta:
        model = Images
        fields = ['title', 'image']
        #fields = ['title']

    def create(self, validated_data):
        """
        Create and return a new `Snippet` instance, given the validated data.
        """
        return Images.objects.create(**validated_data)

    def update(self, instance, validated_data):
        """
        Update and return an existing `Snippet` instance, given the validated data.
        """
        instance.title = validated_data.get('title', instance.title)
        instance.image = validated_data.get('image', instance.image)

        instance.save()
        return instance

class CheckSerializer(serializers.ModelSerializer):
    image = serializers.ImageField(use_url=True)

    class Meta:
        model = Check
        fields = ['title', 'image']


    def create(self, validated_data):
        return Check.objects.create(**validated_data)

    def update(self, instance, validated_data):
        """
        Update and return an existing `Snippet` instance, given the validated data.
        """
        instance.title = validated_data.get('title', instance.title)
        instance.image = validated_data.get('image', instance.image)

        instance.save()
        return instance

