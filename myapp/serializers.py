from rest_framework import serializers
from .models import ProductData

class ProductDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductData
        fields = '__all__'
