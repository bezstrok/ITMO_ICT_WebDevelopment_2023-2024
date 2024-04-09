from django.utils.translation import gettext_lazy as _
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from backend.broker.models import Broker
from backend.product.models import Product, ProductBatch
from backend.trade.models import Trade


class TradeProductBatchProductSerializer(serializers.ModelSerializer):
    manufacturer = serializers.SlugRelatedField(slug_field='firm_name', read_only=True)
    
    class Meta:
        model = Product
        fields = (
            'id', 'name', 'unique_code',
            'category', 'manufacturer'
        )


class TradeProductBatchSerializer(serializers.ModelSerializer):
    product = TradeProductBatchProductSerializer(read_only=True)
    
    class Meta:
        model = ProductBatch
        fields = (
            'id', 'product', 'quantity',
            'price', 'delivery_conditions'
        )


class TradeBrokerSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(source='user.email', read_only=True)
    full_name = serializers.CharField(source='user.full_name', read_only=True)
    firm = serializers.SlugRelatedField(slug_field='name', read_only=True)
    
    class Meta:
        model = Broker
        fields = (
            'id', 'email', 'full_name',
            'firm', 'trades_conducted_count'
        )


class RetrieveTradeSerializer(serializers.ModelSerializer):
    broker = TradeBrokerSerializer(read_only=True)
    product_batch = TradeProductBatchSerializer(read_only=True)
    
    class Meta:
        model = Trade
        fields = (
            'id', 'start_time', 'end_time',
            'status', 'total_amount', 'broker',
            'product_batch'
        )


class ListTradeSerializer(serializers.ModelSerializer):
    broker = serializers.CharField(source='broker.user.full_name', read_only=True)
    product = serializers.CharField(source='product_batch.product.name', read_only=True)
    quantity = serializers.IntegerField(source='product_batch.quantity', read_only=True)
    
    class Meta:
        model = Trade
        fields = (
            'id', 'start_time', 'end_time',
            'status', 'total_amount', 'broker',
            'product', 'quantity'
        )


class UpdateDeleteTradeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Trade
        fields = (
            'id', 'status', 'total_amount'
        )


class CreateTradeSerializer(serializers.ModelSerializer):
    product_batch = serializers.PrimaryKeyRelatedField(queryset=ProductBatch.objects.all())
    
    class Meta:
        model = Trade
        fields = (
            'id', 'total_amount', 'product_batch'
        )
    
    def validate_product_batch(self, value):
        if not value.is_available:
            raise ValidationError(_('The selected product batch is not available for trading.'))
        return value
