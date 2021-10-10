  
from rest_framework import serializers
from profiles.models import Profile

class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        #fields = ['id', 'studentId', 'name']
        fields = ['id', 'studentId', 'check']

    def create(self, validated_data):
        
        return Profile.objects.create(**validated_data)

    def update(self, instance, validated_data):
        
        instance.studentId = validated_data.get('studentId', instance.studentId)
        instance.check = validated_data.get('check', instance.check)
        instance.save()
        return instance
