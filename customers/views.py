import random
from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from .models import Profile
from django.contrib.auth.models import User
import os
from twilio.rest import Client

# Find these values at https://twilio.com/user/account
# To set up environmental variables, see http://twil.io/secure
account_sid = 'AC1e43cfeea46379c2f8fbd83ea39d336c'
auth_token = 'c569ee15f7e4277e27bdc5de94ad5562'

def send_otp(mobile, otp):
    try:
        client = Client(account_sid, auth_token)
        client.api.account.messages.create(
            to="+919391962924",
            from_="+14786072077",
            body="Message from dormet your otp is {}".format(otp))
        print(client)
    except:
        print("Something went wrong")
    
    return 
# Create your views here.
@api_view(['GET'])
def home(request):
    return Response("therre")

@api_view(['POST'])
def verify_otp(request):
    mobile = request.POST.get('mobile')
    if request.method == 'POST':
        otp = request.POST.get('otp')
        print(otp)
        if otp != '':
            profile = Profile.objects.filter(mobile_number=mobile).first()
            if profile.otp == int(otp):
                return Response({"message":"success"})
            else:
                return Response({"message":"Wrong otp please try again"})
        else:
            return Response({"message":"Cannot be empty"})

@api_view(['POST'])
def account_login(request):
    if request.method == 'POST':
        mobile = request.POST.get('mobile')
        if(mobile != ''): 
            otp = int(random.randint(1000,9999))
            send_otp(mobile, otp)
            check_user = Profile.objects.filter(mobile_number=mobile)
            if check_user:
                exists_user = Profile.objects.get(mobile_number=mobile)
                exists_user.otp = otp
                exists_user.save()
                request.session['mobile'] = mobile
                return Response({"message":"success","otp":exists_user.otp})
            else:
                user = User.objects.create_user(username=mobile,password="zxcvbnm321")
                user.save()
                profile = Profile.objects.create(user=user,mobile_number=mobile,otp=otp)
                profile.save()
                token, created = Token.objects.get_or_create(user=user)
                request.session['mobile'] = mobile
                request.session['token'] = token.key
        else:
            return Response({"message":"Cannot be empty"})
    return Response({"message":"success","otp":profile.otp})



