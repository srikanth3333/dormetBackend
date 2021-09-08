import random
from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from .models import Profile
from django.contrib.auth.models import User

# Create your views here.
@api_view(['GET'])
def home(request):
    return Response("therre")

@api_view(['POST'])
def verify_otp(request):
    mobile = request.session.get('mobile')
    token = request.session.get('token')
    if request.method == 'POST':
        otp = request.POST.get('otp')
        profile = Profile.objects.filter(mobile_number=mobile).first()
        if profile.otp == int(otp):
            return Response({"message":"Logged In Successfully","token":token})
        else:
            return Response({"message":"Wrong otp please try again"})

@api_view(['POST'])
def account_login(request):
    if request.method == 'POST':
        mobile = request.POST.get('mobile')
        # check_user = Profile.objects.filter(mobile_number=mobile)
        user = User(username=mobile)
        user.save()
        otp = int(random.randint(1000,9999))
        profile = Profile.objects.create(user=user,mobile_number=mobile,otp=otp)
        profile.save()
        token, created = Token.objects.get_or_create(user=user)
        request.session['mobile'] = mobile
        request.session['token'] = token.key
    return Response({"message":"User Created Successfully","otp":profile.otp})



