from django.urls import path
from .views import CustomUserCreate, BlacklistTokenUpdateView, GetUserDetail

app_name = 'users'

urlpatterns = [
    path('', GetUserDetail.as_view(), name="get_user"),
    path('register/', CustomUserCreate.as_view(), name="create_user"),
    path('logout/blacklist/', BlacklistTokenUpdateView.as_view(), name='blacklist')
]