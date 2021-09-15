from .models import Category
from .serializers import CategorySerializer
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication, SessionAuthentication
from rest_framework.authtoken.models import Token
from products.models import Products
from products.serializers import ProductSerializer
from django.db.models import Q

# Views
@api_view(['POST'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def add_category(request):
    if request.method == 'POST':
        category_name = request.POST.get('category_name')
        token = request.headers.get('Authorization')
        user = Token.objects.get(key=token[6:]).user
        category = Category.objects.create(user =user,category_name=category_name)
        category.save()
        return Response({"message":"Category Added Successfully","name":category_name})
    

@api_view(['GET'])
def get_categories(request):
    categories = Category.objects.all()
    serializer = CategorySerializer(categories, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def get_category_products(request,pk):
    products = Products.objects.filter(shop__id=pk)
    serializer = ProductSerializer(products, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def search_products(request):
    search_text = request.GET.get('q')
    # offer_price
    # tag_name
    # category
    # products_description
    products = Products.objects.filter(Q(product_name__icontains=search_text) | Q(price__icontains=search_text ))
    print(products)
    serializer = ProductSerializer(products, many=True)
    return Response(serializer.data)