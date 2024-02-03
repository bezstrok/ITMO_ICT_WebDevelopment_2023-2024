from rest_framework import serializers

from backend.broker.models import Broker, Firm


class FirmBrokerSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(source='user.email', read_only=True)
    full_name = serializers.CharField(source='user.full_name', read_only=True)
    
    class Meta:
        model = Broker
        fields = ('id', 'profit_percentage', 'fixed_monthly_amount', 'email', 'full_name')


class FirmDetailSerializer(serializers.ModelSerializer):
    brokers = FirmBrokerSerializer(read_only=True, many=True)
    
    class Meta:
        model = Firm
        fields = ('id', 'name', 'address', 'brokers_count', 'brokers')


class FirmListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Firm
        fields = ('id', 'name', 'address', 'brokers_count')
