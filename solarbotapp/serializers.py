from rest_framework import serializers
from .models import *
import re
from django.utils import timezone as dt

class create_product_serializer(serializers.Serializer):
    product_code=serializers.CharField(required=True)
    product_name=serializers.CharField(required=True)
    vendor_name=serializers.CharField(required=True)
    category=serializers.CharField(required=True)
    sub_category=serializers.CharField(required=True)
    retail_price=serializers.FloatField(required=True)
    cost_price=serializers.FloatField(required=True)
    quantity=serializers.IntegerField(required=True)
    
    def validate(self, attrs):
        product_code=attrs.get('product_code')
        regex = r'^[a-zA-Z0-9-]*$'
        product=products.objects.filter(product_code=product_code)
        if product.exists():
            print(product)
            raise serializers.ValidationError("Product Code already exists")
        if not (re.match(regex, product_code)):
            raise serializers.ValidationError("Product Code cannot have special characters other than -")
        
        return attrs

class producct_file_list(serializers.ModelSerializer):
    class Meta:
        model = product_file
        fields = '__all__'

class product_list_serializer(serializers.ModelSerializer):
    files = serializers.SerializerMethodField()
    def get_files(self,obj):
        serializer = producct_file_list(product_file.objects.filter(product_code=obj.product_code),many=True)
        return serializer.data

    class Meta:
        model = products
        # fields =['id','product_code','product_name']
        exclude = ('file_upload',)

class product_detail_serializer(serializers.ModelSerializer):
    files = serializers.SerializerMethodField()
    def get_files(self,obj):
        serializer = producct_file_list(product_file.objects.filter(product_code=obj.product_code),many=True)
        return serializer.data
    
    class Meta:
        model = products
        # fields = ['product_code','product_name','product_description','category','quantity','product_group','retail_price','cost_price','updated_time','image','file_upload']
        fields = '__all__'

class update_product_serializer(serializers.Serializer):
    files = serializers.SerializerMethodField()
    def get_files(self,obj):
        serializer = producct_file_list(product_file.objects.filter(product_code=obj.product_code),many=True)
        return serializer.data

    product_name =serializers.CharField(required=False)
    # product_descr=serializers.CharField(required=False)
    vendor_name=serializers.CharField(required=False)
    category=serializers.CharField(required=False)
    sub_category=serializers.CharField(required=False)
    retail_price=serializers.FloatField(required=False)
    cost_price=serializers.FloatField(required=False)
    quantity=serializers.IntegerField(required=False)
    image = serializers.ImageField(required=False)
    # file_upload = serializers.FileField(required=False)

    def update_(self,instance,validated_data):
        product = instance
        product.state_manager = dt.now()
        product.save()
        instance.id = None
        instance.product_name = validated_data['product_name']
        instance.vendor_name = validated_data['vendor_name']
        instance.category = validated_data['category']
        instance.sub_category = validated_data['sub_category']
        instance.retail_price = validated_data['retail_price']
        instance.cost_price = validated_data['cost_price']
        instance.quantity = validated_data['quantity']
        instance.image = validated_data['image']
        instance.state_manager = None
        instance.save()

