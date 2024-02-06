from rest_framework import serializers

from backend.manufacturer.models import Manufacturer
from backend.product.models import Product, ProductBatch


class ProductManufacturerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Manufacturer
        fields = (
            'id', 'firm_name', 'products_count'
        )


class ProductProductBatchSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductBatch
        fields = (
            'id', 'batch_number', 'quantity',
            'price'
        )


class RetrieveProductSerializer(serializers.ModelSerializer):
    manufacturer = ProductManufacturerSerializer(read_only=True)
    
    class Meta:
        model = Product
        fields = (
            'id', 'name',
            'unique_code', 'category', 'weight',
            'production_date', 'expiry_date', 'measurement_unit',
            'manufacturer', 'batches_count'
        )


class ListProductsSerializer(serializers.ModelSerializer):
    manufacturer = serializers.SlugRelatedField(slug_field='firm_name', read_only=True)
    
    class Meta:
        model = Product
        fields = (
            'id', 'name', 'unique_code',
            'category', 'manufacturer', 'batches_count'
        )


class CRUDProductSerializer(serializers.ModelSerializer):
    manufacturer = serializers.SlugRelatedField(slug_field='firm_name', read_only=True)
    
    class Meta:
        model = Product
        fields = (
            'id', 'name', 'unique_code',
            'category', 'weight', 'production_date',
            'expiry_date', 'measurement_unit', 'manufacturer'
        )
        read_only_fields = ('unique_code',)
