from django.utils import timezone
from django.shortcuts import render, get_object_or_404
from categories.models import Category
from .serializers import ProductSerializer
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from rest_framework.authtoken.models import Token
from .models import OrderedItem, Order, Comments, BillingAddress, Shops, Products
from customers.models import Profile

# Create your views here.
@api_view(['POST'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def add_product(request):
    if request.method == 'POST':
        product_name = request.POST.get('product_name')
        price = request.POST.get('price')
        offer_price = request.POST.get('offer_price')
        tag_name = request.POST.get('tag_name')
        quantity = request.POST.get('quantity')
        category = request.POST.get('category')
        products_description = request.POST.get('products_description')
        ratings = request.POST.get('ratings')
        category_main = Category.objects.get(id=category)
        token = request.headers.get('Authorization')
        user = Token.objects.get(key=token[6:]).user
        # Getting shops and user added products
        # get_product_user = Products.objects.get(user=user)
        get_shop_user = get_object_or_404(Shops, user=user)
        if get_shop_user.user.id == user.id:
            product = Products.objects.create(user=user,product_name=product_name,price=price,
                                            offer_price=offer_price,tag_name=tag_name,quantity=quantity,
                                            category=category_main,products_description=products_description,
                                            ratings=ratings,shop=get_shop_user)
            product.save()
            return Response({"message": "Product Added Successfully"})
        else:
            Response({"message": "You don't have any active shops"})

        return Response({"message": "Something Went Wrong"})

@api_view(['GET'])
def get_products(request):
    products = Products.objects.all()
    serializer = ProductSerializer(products, many=True)
    return Response({"products":serializer.data})


@api_view(['POST'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def add_to_cart(request):
    id = request.POST.get('id')
    token = request.headers.get('Authorization')
    user = Token.objects.get(key=token[6:]).user
    item = get_object_or_404(Products, id=id)
    order_item, created = OrderedItem.objects.get_or_create(item=item,user=user,ordered=False)
    order_qs = Order.objects.filter(user=user,ordered=False)
    if order_qs.exists():
        order = order_qs[0]
        # Getting Current Shop
        # print(item.shop.shop_name) 
        # Getting Cart Shop
        if order.items.filter(item__id=id).exists():
            order_item.quantity += 1
            order_item.save()
            return Response({"message":"Item Quantity Updated"})
        else:
            order.items.add(order_item)
    else:
        ordered_date = timezone.now()
        order = Order.objects.create(user=user,start_date=ordered_date)
        order.items.add(order_item)
        return Response({"message":"Item Added  to cart"})
    
    return Response({"message":"Item Added  to cart"})


@api_view(['POST'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def remove_from_cart(request):
    id = request.POST.get('id')
    token = request.headers.get('Authorization')
    user = Token.objects.get(key=token[6:]).user
    item = get_object_or_404(Products, id=id)
    order_qs = Order.objects.filter(user=user,ordered=False)
    if order_qs.exists():
        order = order_qs[0]
        if order.items.filter(item__id=id).exists():
            order_item = OrderedItem.objects.filter(item=item,user=user,ordered=False)[0]
            order.items.remove(order_item)
            order_item.delete()
            return Response({"message":"Item removed from cart"})
        else:
            return Response({"message":"You don't have item in your cart"})
    return Response({"message":"cart"})


@api_view(['POST'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def remove_single_item_from_cart(request):
    id = request.POST.get('id')
    token = request.headers.get('Authorization')
    user = Token.objects.get(key=token[6:]).user
    item = get_object_or_404(Products, id=id)
    order_qs = Order.objects.filter(user=user,ordered=False)
    if order_qs.exists():
        order = order_qs[0]
        if order.items.filter(item__id=id).exists():
            order_item = OrderedItem.objects.filter(item=item,user=user,ordered=False)[0]
            if order_item.quantity > 1:
                order_item.quantity -= 1
                order_item.save()
                return Response({"message":"Item Quantity removed"})
            else :
                order_item.delete()
                order.items.remove(order_item)
                return Response({"message":"Item Deleted"})
        else:
            return Response({"message":"Already removed"})

    return Response({"message":"cart"})


@api_view(['POST'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def add_comments(request):
    if request.method == "POST":
        product_id = request.POST.get('product_id')
        text = request.POST.get('comment')
        ratings = request.POST.get('ratings')
        token = request.headers.get('Authorization')
        user = Token.objects.get(key=token[6:]).user
        product = get_object_or_404(Products, id=product_id)
        comments = Comments.objects.create(user=user,product=product,comment=text,rating=int(ratings))
        comments.save()
        return Response({"message":"Comment added successfully"})
    

@api_view(['POST'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def billing_address(request):
    order_id = request.POST.get('order_id')
    first_name = request.POST.get('first_name')
    last_name = request.POST.get('last_name')
    email = request.POST.get('email')
    address1 = request.POST.get('address1')
    address2 = request.POST.get('address2')
    pincode = request.POST.get('pincode')
    city = request.POST.get('city')
    state = request.POST.get('state')
    order = Order.objects.get(id=order_id)
    token = request.headers.get('Authorization')
    user = Token.objects.get(key=token[6:]).user
    billing = BillingAddress(user=user,first_name=first_name, last_name=last_name, email=email, address1=address1,
                            address2=address2,pincode=pincode, state=state, order=order, city=city)
    billing.save()
    order_item = Order.objects.get(user=user,ordered=False)
    order_item.billing_address = billing
    order_item.save()

    return Response({"message":"Billing Address Added"})
            

@api_view(['GET'])
def get_products(request):
    products = Products.objects.all()
    serializer = ProductSerializer(products, many=True)
    return Response({"products":serializer.data})


@api_view(['POST'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def shops_create(request):
    if request.method == 'POST':
        token = request.headers.get('Authorization')
        user = Token.objects.get(key=token[6:]).user
        shop_name = request.POST.get('shop_name')
        ratings = request.POST.get('ratings')
        comments = request.POST.get('comments')
        # products = request.POST.get('products')
        shops = Shops.objects.create(user=user,shop_name=shop_name,ratings=ratings,comments=comments)
        shops.save()

        return Response({"message":"Shop Created Successfully"})




@api_view(['POST'])
def order_confimrations(request):
    token = request.headers.get('Authorization')
    user = Token.objects.get(key=token[6:]).user
    order_qs = Order.objects.filter(user=user,ordered=False)
    #check payment

    #then
    if order_qs.exists():
        order = order_qs[0]
        order.ordered = True
        order.save()
        return Response({"message":"Order Successfully Done"})

    return Response({"message":"Something went wrong"})
    