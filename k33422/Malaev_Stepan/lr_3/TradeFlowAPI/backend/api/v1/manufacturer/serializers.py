from django.contrib.auth import get_user_model
from rest_framework import serializers

from backend.manufacturer.models import Manufacturer

User = get_user_model()


class ManufacturerUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'full_name', 'email')


class RetrieveManufacturerSerializer(serializers.ModelSerializer):
    user = ManufacturerUserSerializer(read_only=True)
    
    class Meta:
        model = Manufacturer
        fields = ('id', 'address', 'contact_info', 'user', 'products_count')


class ListManufacturerSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(source='user.email', read_only=True)
    full_name = serializers.CharField(source='user.full_name', read_only=True)
    
    class Meta:
        model = Manufacturer
        fields = ('id', 'address', 'contact_info', 'email', 'full_name', 'products_count')


class CRUDManufacturerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Manufacturer
        fields = ('id', 'address', 'contact_info')
