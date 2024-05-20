from rest_framework import serializers
from .models import User

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'fullname', 'email', 'mobile', 'address']

        

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'fullname', 'email', 'mobile', 'address', 'password']
        
    def to_representation(self, instance):
        representation = super(UserSerializer, self).to_representation(instance)
        representation.pop('password')
        return representation

    def create(self, validated_data):        
        password = validated_data.pop('password', None)
        validated_data.pop('groups', None)
        validated_data.pop('user_permissions', None)
        instance = self.Meta.model(**validated_data)
        if password is not None:
            instance.set_password(password)
        instance.save()
        return instance
    
    def update(self, instance, validated_data):
        password = validated_data.pop('password', None)
        if password is not None:
            instance.set_password(password)
        return super().update(instance, validated_data) 