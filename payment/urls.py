from django.urls import path, include
from rest_framework.routers import DefaultRouter

from payment.views import CheckoutAPIView, PaymentViewSet


app_name = 'payment'

router = DefaultRouter()
router.register(r'', PaymentViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('checkout/<int:pk>/', CheckoutAPIView.as_view(), name='checkout'),

]