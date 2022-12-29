from rest_framework import  status
from rest_framework.response import Response
from django.contrib.auth import get_user_model

from drf_yasg.utils import swagger_auto_schema
from dj_rest_auth.registration.views import RegisterView, SocialLoginView
from rest_framework import permissions
from rest_framework.viewsets import ReadOnlyModelViewSet
from allauth.socialaccount.providers.google.views import GoogleOAuth2Adapter
from allauth.socialaccount.providers.oauth2.client import OAuth2Client

from dj_rest_auth.views import LoginView
from rest_framework.generics import (
    RetrieveAPIView,
    GenericAPIView,
    RetrieveUpdateAPIView,
)
from .serializers import (
    UserRegistrationSerializer,
    PhoneNumberSerializer,
    AddressReadOnlySerializer,
    VerifyPhoneNumberSerializer,
    UserSerializer,
    UserLoginSerializer)
from .models import  PhoneNumber, Address
from .permissions import (IsUserAddressOwner)



User = get_user_model()
class UserRegisterationAPIView(RegisterView):
    """
    Register new users using phone number or email and password.
    """
    serializer_class = UserRegistrationSerializer

    @swagger_auto_schema(operation_summary="Create a user account by signing Up")
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)

        response_data = ''

        email = request.data.get('email', None)
        phone_number = request.data.get('phone_number', None)
        
        if email and phone_number:
            return Response(data=serializer.data, status=status.HTTP_201_CREATED)

        return Response(data=serializer.data, status=status.HTTP_400_BAD_REQUEST)


class UserLoginAPIView(LoginView):
    """
    Authenticate existing users using phone number or email and password
    """
    serializer_class = UserLoginSerializer


class SendOrResendSMSAPIView(GenericAPIView):
    """
    Check if submitted phone number is a valid phone number and sent OTP.
    """
    serializer_class = PhoneNumberSerializer

    @swagger_auto_schema(operation_summary="Send or resend SMS.")
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():
            # Send OTP
            phone_number = str(serializer.validated_data['phone_number'])

            user = User.objects.filter(
                phone__phone_number = phone_number).first()

            sms_verification = PhoneNumber.objects.filter(
                user=user, is_verified=False).first()

            sms_verification.send_confirmation()
            
            return Response(status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            

class VerifyPhoneNumberAPIView(GenericAPIView):
    """
    Check if submitted phone number and OTP matches and verify the user.
    """
    serializer_class = VerifyPhoneNumberSerializer

    def post(self, request, *args, **kwargs):
        seriallizer = self.get_serializer(data=request.data)

        if seriallizer.is_valid():
            message = {'detail': _('Phone number successfully verified.')}
            return Response(message, status=status.HTTP_200_OK)
        
        return Response(seriallizer.errors, status=status.HTTP_400_BAD_REQUEST)

class GoogleLogin(SocialLoginView):
    """
    Social authentication with Google
    """
    adapter_class = GoogleOAuth2Adapter
    callback_url = "call_back_url"
    client_class = OAuth2Client



class UserAPIView(RetrieveAPIView):
    """
    Get user details
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def get_object(self): 
        return self.request.user

class AddressViewSet(ReadOnlyModelViewSet):
    """
    List and Retrieve user addresses
    """
    queryset = Address.objects.all()
    serializer_class = AddressReadOnlySerializer
    permission_classes = (IsUserAddressOwner,)

    def get_queryset(self):
        res = super().get_queryset()
        user = self.request.user
        return res.filter(user=user)