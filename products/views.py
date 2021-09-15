from django.utils import timezone
from django.shortcuts import get_object_or_404
from categories.models import Category
from .serializers import ProductSerializer, ShopsSerializer, ProductRatingsSerializer, OrderSerializer, OrderedItemSerializer, BillingSerializer, ProfileSerializer, FavouritesSerializer
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from rest_framework.authtoken.models import Token
from .models import OrderedItem, Order, Comments, BillingAddress, Shops, Products, ProductRatings, Favourites
from django.core.exceptions import ObjectDoesNotExist
from customers.models import Profile
from django.contrib.auth.models import User


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


@api_view(['GET'])
def product_detail(request,pk):
    products = get_object_or_404(Products, pk=pk)
    serializer = ProductSerializer(products)
    # data= json.dumps(serializer.data)
    return Response(serializer.data)

@api_view(['GET'])
def productRatings(request,pk):
    ratings = ProductRatings.objects.filter(product__id=pk)
    serializer = ProductRatingsSerializer(ratings, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def all_ratings(request):
    ratings = ProductRatings.objects.all()
    serializer = ProductRatingsSerializer(ratings, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def shopProducts(request,pk):
    products = Products.objects.filter(shop__id=pk)
    print(products)
    serializer = ProductSerializer(products, many=True)
    return Response(serializer.data)

@api_view(['POST'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def add_product_ratings(request):
    if request.method == 'POST':
        id  = request.POST.get('id')
        rating  = request.POST.get('rating')
        comment = request.POST.get('comment')
        token = request.headers.get('Authorization')
        user = Token.objects.get(key=token[6:]).user
        product = Products.objects.get(id=id)
        check_ratings = ProductRatings.objects.filter(user__id=user.id,product__id=id)
        if check_ratings:
            return Response({"Msg":"You've already added ratings"})
        ratings = ProductRatings.objects.create(user=user,product=product,ratings=rating,comment=comment)
        ratings.save()
        return Response({"msg":"Rating Added Successfully"})
    return Response({"msg":"Unable to connect"})


@api_view(['GET'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def cart_count(request):
    token = request.headers.get('Authorization')
    user = Token.objects.get(key=token[6:]).user
    order_qs = Order.objects.get(user=user,ordered=False)
    count = order_qs.items.count()
    return Response({"count":count})

@api_view(['POST'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def add_to_cart(request):
    id = request.POST.get('id')
    token = request.headers.get('Authorization')
    quantity = request.POST.get('quantity')
    user = Token.objects.get(key=token[6:]).user
    item = get_object_or_404(Products, id=id)
    shop = Shops.objects.get(shop_name=item.shop.shop_name)
    order_item, created = OrderedItem.objects.get_or_create(item=item,user=user,ordered=False)
    order_item.quantity_in_grams = quantity 
    order_item.shop = shop
    order_item.save()
    order_qs = Order.objects.filter(user=user,ordered=False)
    if order_qs.exists():
        order = order_qs[0]
        if order.items.filter(item__id=id).exists() and item.shop.shop_name == order_item.shop.shop_name:
            order_item.quantity_in_grams = quantity
            order_item.quantity += 1
            order_item.save()
            return Response({"message":"Item Quantity Updated"})
        else:
            get_order_item = OrderedItem.objects.filter(user=user,ordered=False).exclude(shop__shop_name=order_item.shop.shop_name)
            if get_order_item.exists():
                get_order_item.delete()
                order.items.add(order_item)
                return Response({"message":"Added From Another Shop"})
            else:
                order.items.add(order_item)
                return Response({"message":"Added New Product From Same Shop"})
    else:
        ordered_date = timezone.now()
        order = Order.objects.create(user=user,start_date=ordered_date)
        order.items.add(order_item)
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

@api_view(['GET'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def review(request):
    token = request.headers.get('Authorization')
    user = Token.objects.get(key=token[6:]).user
    order_qs = Order.objects.filter(user=user,ordered=False)
    serializer = OrderSerializer(order_qs, many=True)
    return Response(serializer.data)


@api_view(['POST'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def payment(request):
    amount = request.POST.get('amount')
    shop_name = request.POST.get('shop_name')
    payment_id = request.POST.get('payment_id')
    order_id = request.POST.get('order_id')
    token = request.headers.get('Authorization')
    user = Token.objects.get(key=token[6:]).user
    order_qs = Order.objects.filter(user=user,ordered=False)
    shop = Shops.objects.get(shop_name=shop_name)
    
    if order_qs.exists():
        order = order_qs[0]
        order.ordered = True
        order.amount = amount
        order.payment_id = payment_id
        order.payment_status = True
        order.order_id = order_id
        order.shop = shop
        for i in order.items.all():
            order_item = OrderedItem.objects.get(user=user,ordered=False,id=i.id)
            order_item.ordered = True
            order_item.save()
            print(i.id)
        order.save()
        
        return Response({"message":"Success"})

    return Response({"message":"Payment Failed"})


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
    

@api_view(['GET','POST','PUT'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def billing_address(request):
    
    if request.method == 'GET':
        token = request.headers.get('Authorization')
        user = Token.objects.get(key=token[6:]).user
        address = BillingAddress.objects.filter(user=user)
        serializer = BillingSerializer(address, many=True)
        return Response({"message":serializer.data})
    
    if request.method == 'POST':
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        address1 = request.POST.get('address1')
        address2 = request.POST.get('address2')
        pincode = request.POST.get('pincode')
        city = request.POST.get('city')
        state = request.POST.get('state')
        token = request.headers.get('Authorization')
        user = Token.objects.get(key=token[6:]).user
        order_item = Order.objects.get(user=user,ordered=False)
        billing = BillingAddress(user=user,first_name=first_name, last_name=last_name, email=email, address1=address1,
                                address2=address2,pincode=pincode, state=state, order=order_item, city=city)
        billing.save()
        order_item.billing_address = billing
        order_item.save()
        return Response({"message": "Added Address"}) 

    if request.method == "PUT":
        id = request.POST.get('id')
        token = request.headers.get('Authorization')
        user = Token.objects.get(key=token[6:]).user
        billing = BillingAddress.objects.get(user=user,id=id)
        order_item = Order.objects.get(user=user,ordered=False)
        order_item.billing_address = billing
        order_item.save()
        return Response({"message": "Address Assigned"}) 



@api_view(['GET'])
def get_shops(request):
    shops = Shops.objects.all()
    serializer = ShopsSerializer(shops, many=True)
    return Response({"shops":serializer.data})


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
    if order_qs.exists():
        order = order_qs[0]
        order.ordered = True
        order.save()
        return Response({"message":"Order Successfully Done"})

    return Response({"message":"Something went wrong"})
    



@api_view(['GET'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def cart_list(request):
    # discount = request.POST.get('discount')
    token = request.headers.get('Authorization')
    user = Token.objects.get(key=token[6:]).user
    order_qs = OrderedItem.objects.filter(user=user,ordered=False)
    serializer = OrderedItemSerializer(order_qs, many=True)
    total_price = 0
    for i in order_qs:
        if i.item.offer_price:
            total_price += int(i.item.offer_price) * int(i.quantity)
        else:
           total_price += int(i.item.price) * int(i.quantity)
    final_price = total_price + 50
    count = order_qs.count()
    return Response({"cart":serializer.data,"total":final_price,"cart_Count":count})


@api_view(['GET'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def my_orders(request):
    token = request.headers.get('Authorization')
    user = Token.objects.get(key=token[6:]).user
    order_qs = Order.objects.filter(user=user,ordered=True)
    if order_qs:
        serializer = OrderSerializer(order_qs, many=True)
        return Response(serializer.data)
    
    return Response({"message":"No orderes found"})



@api_view(['POST'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def track_order(request,pk):
    token = request.headers.get('Authorization')
    user = Token.objects.get(key=token[6:]).user
    order = Order.objects.get(id=pk,user=user,ordered=True)
    serializer = OrderSerializer(order)
    return Response(serializer.data)



@api_view(['POST'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def order_summary(request,pk):
    product_list = []
    token = request.headers.get('Authorization')
    user = Token.objects.get(key=token[6:]).user
    order = Order.objects.get(user=user,ordered=True,id=pk)
    for i in order.items.all():
        product_list.append(i.item.id)
    products = Products.objects.filter(id__in=product_list)
    product_serializer = ProductSerializer(products, many=True)
    return Response(product_serializer.data)


@api_view(['GET','POST'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def profile(request):

    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        mobile_number = request.POST.get('mobile')
        # image = request.data['image']
        token = request.headers.get('Authorization')
        user = Token.objects.get(key=token[6:]).user
        profile = Profile.objects.get(user=user)
        main_user = User.objects.get(username=user.username)
        profile.email = email
        profile.name = name
        profile.mobile_number = mobile_number
        # profile.profile_image = image
        profile.save()
        main_user.first_name = name
        main_user.email = email
        main_user.save()
        return Response({"msg": "Profile Updated"})

    if request.method == 'GET':
        token = request.headers.get('Authorization')
        user = Token.objects.get(key=token[6:]).user
        profile = Profile.objects.get(user=user)
        serializer = ProfileSerializer(profile)
        return Response(serializer.data)

    

    return Response("Wrong Method")

@api_view(['GET','POST','DELETE'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def favourites(request):

    if request.method == 'GET':
        product_list = []
        token = request.headers.get('Authorization')
        user = Token.objects.get(key=token[6:]).user
        favourite_list = Favourites.objects.get(user=user)
        for i in favourite_list.product.all():
            product_list.append(i.id)
        products = Products.objects.filter(id__in=product_list)
        product_serializer = ProductSerializer(products, many=True)
        return Response(product_serializer.data)
    
    if request.method == 'POST':
        id = request.POST.get('id')
        item = get_object_or_404(Products,id=id)
        token = request.headers.get('Authorization')
        user = Token.objects.get(key=token[6:]).user
        favourite, created = Favourites.objects.update_or_create(user=user)
        if created:
            favourite.product.add(item)
            favourite.save()
        else:
            favourite.product.add(item)
            favourite.save()
        return Response({"msg":"Added to favourite"})

    if request.method == 'DELETE':
        id = request.POST.get('id')
        item = get_object_or_404(Products,id=id)
        token = request.headers.get('Authorization')
        user = Token.objects.get(key=token[6:]).user
        favourite= Favourites.objects.get(user=user)
        favourite.product.remove(item)
        favourite.save()
        return Response({"msg":"Removed from favourite"})

    return Response("Wrong Method")