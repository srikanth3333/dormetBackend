from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from products.models import Order
from rest_framework.authtoken.models import Token
from customers.models import Profile
from .models import Retailer,DeliveryAgent
from django.contrib.auth.models import User

# Create your views here.
@api_view(['POST'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def delivery(request):
    delivery_agent_id = request.POST.get('delivery_agent_id')
    token = request.headers.get('Authorization')
    user = Token.objects.get(key=token[6:]).user
    profile = Profile.objects.get(user=user)
    order_item = Order.objects.filter(ordered=True,being_delivered=False,retailer_assigned=False)
    print(order_item)
    delivery_user = User.objects.get(id=delivery_agent_id)
    if order_item.exists():
        order = order_item[0]
        print(profile.role)
        if profile.role == '3':
            agent = DeliveryAgent.objects.create(user=delivery_user, location="location",delivered=False)
            agent.save()
            retailer = Retailer.objects.create(user=user,assigned_agent=agent,assigned_order_complete=True)
            retailer.save()
            order.retailer_assigned = True
            order.save()
            return Response({"message":"Successfully assigned to delivery person"})


    return Response({"message":"Something went wrong"})


@api_view(['POST'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def order_submission(request):
    token = request.headers.get('Authorization')
    user = Token.objects.get(key=token[6:]).user
    order_item = Order.objects.get(ordered=True,being_delivered=False,retailer_assigned=True)
    agent = DeliveryAgent.objects.get(user=user)
    order_item.being_delivered = True
    order_item.save()
    agent.delivered = True
    agent.save()
    return Response({"message":"Order Delivered"})
