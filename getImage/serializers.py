from rest_framework import serializers
from getImage.models import Image  
from django.core.files import File
import base64


class ImageSerializer(serializers.ModelSerializer):
    image = serializers.ImageField(use_url=True)

    class Meta:
        model = Image
        fields = ['title', 'image']
        #fields = ['title']

#    def get_base64_image(self, obj):
#        f = open(obj.image_file.path, 'rb')
#        image = File(f)
#        data = base64.b64encode(image.read())
#        f.close()
#        return data


    def create(self, validated_data):
        """
        Create and return a new `Snippet` instance, given the validated data.
        """
        return Image.objects.create(**validated_data)

    def update(self, instance, validated_data):
        """
        Update and return an existing `Snippet` instance, given the validated data.
        """
        instance.title = validated_data.get('title', instance.title)
        instance.image = validated_data.get('image', instance.image)

        instance.save()
        return instance
