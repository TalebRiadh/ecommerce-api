from rest_framework import serializers
import json

from .models import Product, ProductCategory

from django_elasticsearch_dsl_drf.serializers import DocumentSerializer
from .documents import *

class ProductCategoryReadSerializer(serializers.ModelSerializer):
    """
    Serializer class for product categories
    """
    class Meta: 
        model = ProductCategory
        fields = '__all__'


class ProductReadSerializer(serializers.ModelSerializer):
    """
    Serializer class for reading products
    """
    seller = serializers.CharField(
        source='seller.get_full_name', read_only=True)
    category = serializers.CharField(
        source='category.name', read_only=True)

    class Meta: 
        model = Product
        fields = '__all__'


class CreateProductSerializer(serializers.ModelSerializer):
    """
    Serializer class for creating products
    """
    seller = serializers.HiddenField(default=serializers.CurrentUserDefault)
    category = ProductCategoryReadSerializer()

    class Meta:
        model = Product
        fields = ('seller', 'category', 'name', 'desc', 'image', 'price', 'quantity',)
    
    def create(self, validated_data):
        category = validated_data.pop('category')
        instance, created = ProductCategory.objects.get_or_create(**category)
        product = Product.objects.create(**validated_data, category=instance)

        return product

    def update(self, instance, validated_data):
        if 'category' in validated_data:
            nested_serializer = self.fields['category']
            nested_instance = instance.category
            nested_data = validated_data.pop('category')
            nested_serializer.update(nested_instance, nested_data)

        return super(CreateProductSerializer, self).update(instance, validated_data)




class NewsDocumentSerializer(DocumentSerializer):

    class Meta(object):
        """Meta options."""
        model = Product
        document = ProductDocument
        fields = (
            'name',
            'desc',
        )
        def get_location(self, obj):
            """Represent location value."""
            try:
                return obj.location.to_dict()
            except:
                return {}