from rest_framework import routers
from django.urls import include, path
from .views import AuthorizationViewSet

app_name = 'users'


urlpatterns = [
    path('login/', AuthorizationViewSet.as_view({'post': 'login'}), name="authorization"),
    path('signup/', AuthorizationViewSet.as_view({'post': 'signup'}), name="authorization"),
    path('get/', AuthorizationViewSet.as_view({'get': 'get_user'}), name="authorization"),
    path('logout/', AuthorizationViewSet.as_view({'post': 'logout'}), name="authorization"),
    path('change/', AuthorizationViewSet.as_view({'post': 'change_password'}), name="authorization"),
    # path('send_the_email/', AuthorizationViewSet.as_view({'post': 'send_the_email'}), name="authorization"),
    path('send_code/', AuthorizationViewSet.as_view({'post': 'forgot_password'}), name="authorization"),
    path('reset_password/', AuthorizationViewSet.as_view({'post': 'reset_password'}), name="authorization"),
]
