from rest_framework import serializers

from backend.api.v1.broker.serializers import BrokerSerializer
from backend.broker.models import Firm


class FirmDetailSerializer(serializers.ModelSerializer):
    brokers = BrokerSerializer(read_only=True, many=True)
    
    class Meta:
        model = Firm
        fields = ['id', 'name', 'address', 'brokers']


class FirmListSerializer(serializers.ModelSerializer):
    brokers_count = serializers.IntegerField(source='get_brokers_count', read_only=True)
    
    class Meta:
        model = Firm
        fields = ['id', 'name', 'address', 'brokers_count']
