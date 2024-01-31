from django.contrib.auth import get_user_model
from rest_framework import serializers

from backend.broker.models import Broker, Firm
from backend.manufacturer.models import Manufacturer

User = get_user_model()


class ManufacturerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Manufacturer
        fields = ['id', 'address', 'contact_info']


class FirmSerializer(serializers.ModelSerializer):
    class Meta:
        model = Firm
        fields = ['id', 'name', 'address']


class BrokerSerializer(serializers.ModelSerializer):
    firm = FirmSerializer(read_only=True)
    
    class Meta:
        model = Broker
        fields = ['id', 'profit_percentage', 'fixed_monthly_amount', 'firm']


class CurrentUserSerializer(serializers.ModelSerializer):
    roles_serializers = [BrokerSerializer, ManufacturerSerializer]
    
    roles = serializers.SerializerMethodField()
    
    class Meta:
        model = User
        fields = ('id', 'email', 'first_name', 'last_name', 'roles')
        read_only_fields = ('email',)
    
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
        fields = ('id', 'email')
        read_only_fields = ('email',)
