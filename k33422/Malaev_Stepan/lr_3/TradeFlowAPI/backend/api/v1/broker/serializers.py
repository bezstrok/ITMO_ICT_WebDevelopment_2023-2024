from django.contrib.auth import get_user_model
from rest_framework import serializers

from backend.broker.models import Broker, Firm

User = get_user_model()


class BrokerUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'full_name', 'email')


class RetrieveBrokerFirmSerializer(serializers.ModelSerializer):
    class Meta:
        model = Firm
        fields = ('id', 'name', 'address', 'brokers_count')


class ListBrokerFirmSerializer(serializers.ModelSerializer):
    class Meta:
        model = Firm
        fields = ('id', 'name')


class RetrieveBrokerSerializer(serializers.ModelSerializer):
    user = BrokerUserSerializer(read_only=True)
    firm = RetrieveBrokerFirmSerializer(read_only=True)
    
    class Meta:
        model = Broker
        fields = ('id', 'profit_percentage', 'fixed_monthly_amount', 'user', 'firm')


class CRUDBrokerSerializer(serializers.ModelSerializer):
    firm = serializers.PrimaryKeyRelatedField(queryset=Firm.objects.all())
    
    class Meta:
        model = Broker
        fields = ('id', 'profit_percentage', 'fixed_monthly_amount', 'firm')


class ListBrokersSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(source='user.email', read_only=True)
    full_name = serializers.CharField(source='user.full_name', read_only=True)
    firm = ListBrokerFirmSerializer(read_only=True)
    
    class Meta:
        model = Broker
        fields = ('id', 'profit_percentage', 'fixed_monthly_amount', 'email', 'full_name', 'firm')
