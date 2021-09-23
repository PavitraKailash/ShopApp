import datetime

from django.shortcuts import render
from .models import *
from .serializers import *
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, viewsets
from django.contrib.auth.hashers import make_password
from rest_framework.decorators import action


# Create your views here.
class UserViewSet(APIView):
    permission_classes = []

    def post(self, request):
        data = request.data
        username = data['username']
        f_name = data['first_name']
        l_name = data['last_name']
        email = data['email']
        password = data['password']
        phone = data['cst_phone']
        seller = data['is_seller']
        hash_password = make_password(password)
        try:
            user_obj = {}
            user_obj["username"] = username
            user_obj["first_name"] = f_name
            user_obj["last_name"] = l_name
            user_obj["email"] = email
            user_obj["password"] = hash_password
            usr_save = User.objects.create(**user_obj)
            cst_dt = {}
            cst_dt["user_id"] = usr_save
            cst_dt["cst_phone"] = phone
            cst_dt["is_seller"] = seller
            prdt_dt = Customers.objects.create(**cst_dt)

            return Response({"message": "User created successfully"}, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({"message": str(e)}, status=status.HTTP_400_BAD_REQUEST)


class ProductViewset(APIView):
    def post(self, request):
        user = request.user.username
        user_id = User.objects.get(username=user).pk
        if Customers.objects.filter(user_id=user_id, is_seller=True).exists():
            data = request.data
            prd_serializer = ProductSerializer(data=data, many=True)
            if prd_serializer.is_valid():
                prd_serializer.save()
                return Response(prd_serializer.data, status=status.HTTP_200_OK)
            return Response(prd_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response("You are not Seller", status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, pdt_id):
        user = request.user.username
        user_id = User.objects.get(username=user).pk
        if Customers.objects.filter(user_id=user_id, is_seller=True).exists():
            data = request.data
            instance = ProductDetails.objects.get(pdt_id=pdt_id)
            serialzier = ProductSerializer(instance, data=data, partial=True)
            if serialzier.is_valid():
                serialzier.save()
                return Response(serialzier.data, status=status.HTTP_200_OK)
            return Response(serialzier.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response("You are not Seller", status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pdt_id):
        user = request.user.username
        user_id = User.objects.get(username=user).pk
        if Customers.objects.filter(user_id=user_id, is_seller=True).exists():
            try:
                product = ProductDetails.objects.get(pdt_id=pdt_id)
                product.delete()
                return Response(
                    {"code": "200", "message": "Product Deleted"}, status=status.HTTP_200_OK
                )
            except Exception as e:
                return Response(
                    {"code": "400", "message": "Product Not Found"},
                    status=status.HTTP_400_BAD_REQUEST,
                )
        else:
            return Response("You are not Seller", status=status.HTTP_400_BAD_REQUEST)


class ProductListView(APIView):
    permission_classes = []

    def get(self, request):
        product = ProductDetails.objects.all()
        serializer = ProductSerializer(product, many=True).data
        return Response(serializer, status=status.HTTP_200_OK)


class AddToCartView(viewsets.ModelViewSet):
    http_method_names = ["post", "get", "patch"]

    @action(detail=True, methods=["post"])
    def create_cart(self, request):
        user = request.user.username
        user_id = User.objects.get(username=user).pk
        if Customers.objects.filter(user_id=user_id, is_seller=False).exists():
            data = request.data
            prdct = data.get('product')
            qnt = (data.get('quantity') if data.get('quantity') else 1)
            user = request.user.username
            user_id = User.objects.get(username=user).pk
            if not Cart.objects.filter(customer=user_id).exists():
                cart_obj = {}
                cart_obj['customer'] = User.objects.get(username=request.user.username)
                cart_obj['created_at'] = datetime.datetime.now()
                cart_obj['updated_at'] = datetime.datetime.now()
                cart = Cart.objects.create(**cart_obj)
            else:
                cart = Cart.objects.get(customer=user_id)
            if cart:
                if not CartItem.objects.filter(product=prdct, cart=cart).exists():
                    cart_item = {}
                    cart_item["product"] = ProductDetails.objects.get(pdt_id=prdct)
                    cart_item["quantity"] = qnt
                    cart_item["cart"] = cart
                    CartItem.objects.create(**cart_item)
                    return Response("An item has been added", status=status.HTTP_200_OK)
                else:
                    stk = ProductDetails.objects.get(pdt_id=prdct)
                    if stk.stk_no <= 0:
                        return Response("Out of Stock")
                    else:
                        pdt_qnt = CartItem.objects.get(product=prdct, cart=cart)
                        pdt_qnt.quantity = pdt_qnt.quantity + qnt
                        pdt_qnt.save()
                        stk.stk_no = stk.stk_no - qnt
                        stk.save()
                        Cart.objects.filter(pk=cart.pk).update(updated_at=datetime.datetime.now())
                        return Response("Cart Updated", status=status.HTTP_200_OK)
        else:
            return Response("You are not a Customer, Please register yourself as a Customer to continue shopping",
                            status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=["post"])
    def decrement_cart(self, request, pdt_id):
        user = request.user.username
        user_id = User.objects.get(username=user).pk
        if Customers.objects.filter(user_id=user_id, is_seller=False).exists():
            instance = CartItem.objects.get(product=pdt_id)
            instance.quantity = instance.quantity - 1
            instance.save()
            product = ProductDetails.objects.get(pdt_id=pdt_id)
            product.stk_no = product.stk_no +1
            product.save()
            serial = CartItemSerializer(instance)
            return Response(serial.data, status=status.HTTP_200_OK)
        else:
            return Response("You are not a Customer, Please register yourself as a Customer to continue shopping",
                            status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=["post"])
    def empty_cart(self, request, pdt_id):
        user = request.user.username
        user_id = User.objects.get(username=user).pk
        if Customers.objects.filter(user_id=user_id, is_seller=False).exists():
            instance = CartItem.objects.get(product=pdt_id)
            instance.quantity = 0
            instance.save()

            serial = CartItemSerializer(instance)
            return Response(serial.data, status=status.HTTP_200_OK)
        else:
            return Response("You are not a Customer, Please register yourself as a Customer to continue shopping",
                            status=status.HTTP_400_BAD_REQUEST)


class CheckoutOrderView(viewsets.ModelViewSet):

    @action(detail=True, methods=["get"])
    def getOrderDetails(self, request):
        crt = Cart.objects.all()
        serialize = CheckoutSerialier(crt, context={'request': request})
        return Response(serialize.data)

    @action(detail=True, methods=["post"])
    def confirmOrderDetails(self, request):
        try:
            user = request.user.username
            user_id = User.objects.get(username=user).pk
            cart_obj = Cart.objects.get(customer=user_id)
            cart_item = CartItem.objects.filter(cart=cart_obj.pk)
            resp_price = []
            for crt in cart_item:
                quantity = crt.quantity
                prdt = crt.product
                prd_id = ProductDetails.objects.filter(pdt_id=prdt.pk)
                if prdt in prd_id:
                    price = quantity * ProductDetails.objects.get(pdt_id=prdt.pk).pdt_price
                    resp_price.append(price)
            result = sum(resp_price)
            total_item = CartItem.objects.filter(cart=cart_obj.pk).aggregate(Sum('quantity')).get('quantity__sum', 0.00)


            order_obj = {}
            order_obj['cart'] = cart_obj
            order_obj['customer'] = User.objects.get(username=request.user.username)
            order_obj['total_products'] = total_item
            order_obj['total_price'] = result
            Order.objects.create(**order_obj)
            cart_item.delete()
            cart_obj.order_checkout = True
            cart_obj.save()
            return Response("Order Final", status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"message": str(e)}, status=status.HTTP_400_BAD_REQUEST)
