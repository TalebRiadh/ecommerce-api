from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import (
    AddressViewSet,
    SendOrResendSMSAPIView,
    UserAPIView,
    UserLoginAPIView,
    UserRegisterationAPIView,
    VerifyPhoneNumberAPIView,
)

app_name = 'users'

router = DefaultRouter()
router.register(r'', AddressViewSet)

urlpatterns = [
    path('register/', UserRegisterationAPIView.as_view(), name='user_register'),
    path('login/', UserLoginAPIView.as_view(), name='user_login'),

    path(
        'send-sms/',
        SendOrResendSMSAPIView.as_view(),
        name='send_resend_sms'
    ),
    path(
        'verify-phone/',
        VerifyPhoneNumberAPIView.as_view(),
        name='verify_phone_number'
    ),

    path('', UserAPIView.as_view(), name='user_detail'),
    path('address/', include(router.urls)),

]