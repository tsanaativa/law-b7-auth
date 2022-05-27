from django.contrib import admin
from django.urls import path, include
from lawb7auth.views import TokenObtainPairViewLogged, TokenRefreshViewLogged

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/user/', include('users.urls', namespace='users')),
    path('api/token/', TokenObtainPairViewLogged.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshViewLogged.as_view(), name='token_refresh'),
]
