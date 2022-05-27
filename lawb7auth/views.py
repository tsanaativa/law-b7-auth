import json
from django.http import JsonResponse
import jwt
from rest_framework import status
from rest_framework_simplejwt.exceptions import InvalidToken, TokenError

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

from users.models import NewUser
import requests

LOG_URL = 'https://logs-01.loggly.com/inputs/c33818a3-eb2d-4b4f-8d89-6dae5e3993c1/tag/http'

def send_logs(path, method, response):

    payload = {
        'service': 'AUTH_SERVICE',
        'method': method,
        'endpoint': f"https://law-b7-auth.herokuapp.com/api/{path}",
        'response_data': json.loads(response.content),
        'response_status_code': response.status_code,
    }
    print('log payload:', payload)

    result = requests.post(LOG_URL, data=json.dumps(payload))
    if result.status_code != 200:
        print("Auth service gagal mengirim log")
    else:
        print("Auth service sukses mengirim log")

class TokenObtainPairViewLogged(TokenObtainPairView):
    def post(self, request, *args, **kwargs):
        try:
            serializer = self.get_serializer(data=request.data)

            try:
                serializer.is_valid(raise_exception=True)
            except TokenError as e:
                raise InvalidToken(e.args[0])
            response = JsonResponse({'message': f'Access token dan refresh token untuk user dengan email {request.data["email"]} berhasil di-generate.'}, status=status.HTTP_200_OK)
            send_logs('token/', 'POST', response)
            return JsonResponse(serializer.validated_data, status=status.HTTP_200_OK)
        except e:
            response = JsonResponse(e, status=status.HTTP_400_BAD_REQUEST)
            send_logs('token/', 'POST', response)
            return response

class TokenRefreshViewLogged(TokenRefreshView):
    def post(self, request, *args, **kwargs):
        try:
            serializer = self.get_serializer(data=request.data)

            try:
                serializer.is_valid(raise_exception=True)
            except TokenError as e:
                raise InvalidToken(e.args[0])

            user_id = jwt.decode(request.data["refresh"], options={"verify_signature": False})['user_id']
            user = NewUser.objects.get(id=user_id)
            response = JsonResponse({'message': f'Refresh token baru untuk user dengan email {user.email} berhasil di-generate.'}, status=status.HTTP_200_OK)
            send_logs('token/refresh/', 'POST', response)
            return JsonResponse(serializer.validated_data, status=status.HTTP_200_OK)
        except e:
            response = JsonResponse(e, status=status.HTTP_400_BAD_REQUEST)
            send_logs('token/refresh/', 'POST', response)
            return response
