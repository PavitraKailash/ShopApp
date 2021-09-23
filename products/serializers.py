from rest_framework import serializers
from django.contrib.auth.models import User
from .models import *
from django.db.models import Sum


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = "__all__"


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductDetails
        fields = "__all__"


class CartItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = CartItem
        fields = "__all__"


class CheckoutSerialier(serializers.ModelSerializer):
    individual_price = serializers.SerializerMethodField()
    prodct_quantity = serializers.SerializerMethodField()
    total_qnt = serializers.SerializerMethodField()
    total_price = serializers.SerializerMethodField()

    class Meta:
        model = Cart
        fields = ("individual_price", "prodct_quantity", "total_qnt", "total_price")

    def get_total_qnt(self, obj):
        user = None
        request = self.context.get("request")
        if request and hasattr(request, "user"):
            user = request.user
            cart_obj = Cart.objects.get(customer=user.pk)
            cart_item = CartItem.objects.filter(cart=cart_obj.pk).aggregate(Sum('quantity'))
            return cart_item

    def get_individual_price(self, obj):
        user = None
        request = self.context.get("request")
        if request and hasattr(request, "user"):
            user = request.user
            cart_obj = Cart.objects.get(customer=user.pk)
            cart_item = CartItem.objects.filter(cart=cart_obj.pk)
            resp_price = []
            for crt in cart_item:
                quantity = crt.quantity
                prdt = crt.product
                prd_id = ProductDetails.objects.filter(pdt_id=prdt.pk)
                product_name = ProductDetails.objects.get(pdt_id=prdt.pk).pdt_name
                if prdt in prd_id:
                    price = quantity * ProductDetails.objects.get(pdt_id=prdt.pk).pdt_price
                    resp_dict = {
                        product_name: price
                    }
                    resp_price.append(resp_dict)
            return resp_price

    def get_prodct_quantity(self, obj):
        user = None
        request = self.context.get("request")
        if request and hasattr(request, "user"):
            user = request.user
            cart_obj = Cart.objects.get(customer=user.pk)
            cart_item = CartItem.objects.filter(cart=cart_obj.pk)
            resp = []
            for crt in cart_item:
                quantity = crt.quantity
                prdt = crt.product
                prd_id = ProductDetails.objects.filter(pdt_id=prdt.pk)
                product_name = ProductDetails.objects.get(pdt_id=prdt.pk).pdt_name
                if prdt in prd_id:
                    resp_dict = {
                        product_name: quantity
                    }
                    resp.append(resp_dict)
            return resp

    def get_total_price(self,obj):
        user = None
        request = self.context.get("request")
        if request and hasattr(request, "user"):
            user = request.user
            cart_obj = Cart.objects.get(customer=user.pk)
            cart_item = CartItem.objects.filter(cart=cart_obj.pk)
            sum_price = []
            for crt in cart_item:
                quantity = crt.quantity
                prdt = crt.product
                prd_id = ProductDetails.objects.filter(pdt_id=prdt.pk)
                product_name = ProductDetails.objects.get(pdt_id=prdt.pk).pdt_name
                if prdt in prd_id:
                    price = quantity * ProductDetails.objects.get(pdt_id=prdt.pk).pdt_price
                    sum_price.append(price)
            result = sum(sum_price)
            return result



