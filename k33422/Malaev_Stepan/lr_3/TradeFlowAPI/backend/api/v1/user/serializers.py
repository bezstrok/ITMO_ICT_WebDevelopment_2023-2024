from django.contrib.auth import get_user_model
from rest_framework import serializers

from backend.broker.models import Broker, Firm
from backend.manufacturer.models import Manufacturer

User = get_user_model()


class UserManufacturerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Manufacturer
        fields = ('id', 'address', 'contact_info')


class UserBrokerFirmSerializer(serializers.ModelSerializer):
    class Meta:
        model = Firm
        fields = ('id', 'name')


class UserBrokerSerializer(serializers.ModelSerializer):
    firm = UserBrokerFirmSerializer(read_only=True)
    
    class Meta:
        model = Broker
        fields = ('id', 'profit_percentage', 'fixed_monthly_amount', 'firm')


class CurrentUserSerializer(serializers.ModelSerializer):
    roles = serializers.SerializerMethodField()
    
    roles_serializers = (UserBrokerSerializer, UserManufacturerSerializer)
    
    class Meta:
        model = User
        fields = ('id', 'email', 'first_name', 'last_name', 'is_broker', 'is_manufacturer', 'roles')
        read_only_fields = ('email', 'is_broker', 'is_manufacturer')
    
    def get_roles(self, obj):
        data = {}
        
        for serializer in self.roles_serializers:
            model_name = serializer.Meta.model.__name__.lower()
            related_instance = getattr(obj, model_name, None)
            if related_instance:
                data[model_name] = serializer(related_instance).data
        
        return data


class PublicUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'email', 'full_name', 'is_broker', 'is_manufacturer')
        read_only_fields = ('email', 'is_broker', 'is_manufacturer')
