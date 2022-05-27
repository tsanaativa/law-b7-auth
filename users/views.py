import json
from django.http import JsonResponse
import jwt
from rest_framework import status
from rest_framework.views import APIView

from lawb7auth.views import send_logs
from .serializers import RegisterUserSerializer
from .models import NewUser
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework import permissions
import requests

def create_cart(token, user_id, username, email):
    headers = {'Content-type': 'application/json', 'Authorization': 'JWT ' + token}

    payload = {
        "user": {
            "user_id": user_id,
            "username": username,
            "email": email
        }
        
    }
    print('log payload:', payload)

    result = requests.post('https://api-gateway-law.herokuapp.com/cart/create', data=json.dumps(payload), headers=headers)
    if result.status_code != 201:
        print("Cart user gagal dibuat")
    else:
        print("Cart user berhasil dibuat")

class CustomUserCreate(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        print(type(request))
        reg_serializer = RegisterUserSerializer(data=request.data)
        if reg_serializer.is_valid():
            newuser = reg_serializer.save()
            if newuser:
                json = reg_serializer.data
                response = JsonResponse(json, status=status.HTTP_201_CREATED)
                send_logs('user/register/', 'POST', response)
                token = str(RefreshToken.for_user(newuser).access_token)
                create_cart(token, newuser.id, newuser.user_name, newuser.email)
                return response
        response = JsonResponse(reg_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        send_logs('user/register/', 'POST', response)
        return response

class BlacklistTokenUpdateView(APIView):
    permission_classes = [AllowAny]
    authentication_classes = ()

    def post(self, request):
        try:
            refresh_token = request.data["refresh_token"]
            token = RefreshToken(refresh_token)
            user_id = jwt.decode(refresh_token, options={"verify_signature": False})['user_id']
            user = NewUser.objects.get(id=user_id)
            token.blacklist()
            response = JsonResponse({'message': f'User dengan email {user.email} berhasil log out.'}, status=status.HTTP_205_RESET_CONTENT)
            send_logs('user/logout/blacklist/', 'POST', response)
            return response
        except Exception as e:
            print(e)
            response = JsonResponse(e, status=status.HTTP_400_BAD_REQUEST)
            send_logs('user/logout/blacklist/', 'POST', response)
            return response

class GetUserDetail(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        try:
            token = request.headers['Authorization'].split()[1]
            user_id = jwt.decode(token, options={"verify_signature": False})['user_id']
            user = NewUser.objects.get(id=user_id)
            json = dict()
            json['email'] = user.email
            json['user_name'] = user.user_name
            json['first_name'] = user.first_name
            json['last_name'] = user.last_name
            json['phone_number'] = user.phone_number
            response = JsonResponse(json, status=status.HTTP_200_OK)
            send_logs('user/', 'GET', response)
            return response
        except Exception as e:
            print(e)
            response = JsonResponse(e, status=status.HTTP_400_BAD_REQUEST)
            send_logs('user/', 'GET', response)
            return response
