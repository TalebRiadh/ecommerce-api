import datetime
from django.utils import timezone
from django.db import models
from django.conf import settings
from django.contrib.auth.base_user import BaseUserManager
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import AbstractUser
from django.utils.crypto import get_random_string
from rest_framework.exceptions import NotAcceptable
from twilio.rest import Client
from twilio.base.exceptions import TwilioRestException
from phonenumber_field.modelfields import PhoneNumberField
from django_countries.fields import CountryField



    # Create your models here.
class CustomerUserManager(BaseUserManager):
    def create_user(self, email, password, **extra_fields):
        if not email:
            raise ValueError(_('Please enter an email address'))
        email = self.normalize_email(email)
        new_user = self.model(email=email, **extra_fields)
        new_user.set_password(password)
        new_user.save()
        return new_user

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_active', True)
        
        if extra_fields.get('is_superuser') is not True:
            raise ValueError(_('Superuser must have is_superuser=True'))

        if extra_fields.get('is_staff') is not True:
            raise ValueError(_('Superuser must have is_staff=True'))

        return self.create_user(email, password, **extra_fields)


class User(AbstractUser):
    username = models.CharField(_('Username'), max_length=40, unique=True)
    email = models.CharField(_('Email'), max_length=80, unique=True)
    date_joined = models.DateTimeField(_('Date'), auto_now_add=True)

    REQUIRED_FIELDS=['username']
    USERNAME_FIELD='email'
    
    def __str__(self):
        return f"User {self.username}"




class PhoneNumber(models.Model):
    user = models.OneToOneField(
        User, related_name='phone', on_delete=models.CASCADE)
    phone_number = PhoneNumberField(unique=True)
    security_code = models.CharField(max_length=120)
    is_verified = models.BooleanField(default=False)
    sent = models.DateTimeField(null=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ('-created_at',)

    def __str__(self):
        return self.phone_number.as_e164

    def generate_security_code(self):
        """
        returns a unique random 'security_code' for given 'TOKEN_LENGTH' in the settings
        default token length = 6
        """
        token_length = getattr(settings, "TOKEN_LENGTH", 6)
        return get_random_string(token_length, allowed_chars="0123456789")

    def is_security_code_expired(self):
        expiration_date = self.sent + datetime.timedelata(
            minutes = settings.TOKEN_EXPIRE_MINUTES
        )
        return expiration_date <= timezone.now()

    def send_confirmation(self):
        twilio_account_sid = settings.TWILIO_ACCOUNT_SID
        twilio_auth_token = settings.TWILIO_AUTH_TOKEN
        twilio_phone_number = settings.TWILIO_PHONE_NUMBER

        self.security_code = self.generate_security_code()

        print(f'Sending security code {self.security_code} to phone {self.phone_number}')

        if all(
            [
            twilio_account_sid,
            twilio_auth_token,
            twilio_phone_number
            ]
        ):
            try:
                twilio_client = Client(
                    twilio_account_sid, twilio_auth_token
                )
                twilio_client.messages.create(
                    body=f'Your activation code is {self.security_code}',
                    to=str(self.phone_number),
                    from_=twilio_phone_number,
                )
                self.sent = timezone.now()
                self.save()
                return True
            except TwilioRestException as e:
                print(e)
        else:
            print("Twilio credentials are not set")

    def check_verification(self, security_code):
        if(
            not self.is_security_code_expired() and 
            security_code == self.security_code and 
            self.is_verified == False
        ):
            self.is_verified = True
            self.save()
        else:
            raise NotAcceptable(
                _("Your security code is wrong, expired or this phone is verified before."))

        return self.is_verified

class Address(models.Model):
    #Address options
    BILLING = 'B'
    SHIPPING = 'S'

    ADDRESS_CHOICES = ((BILLING, _('billing')), (SHIPPING, _('shipping')))

    user = models.ForeignKey(User, related_name='addresses', on_delete=models.CASCADE)
    address_type = models.CharField(max_length=1, choices=ADDRESS_CHOICES)
    default = models.BooleanField(default=False)
    country = CountryField()
    city = models.CharField(max_length=100)
    street_address = models.CharField(max_length=100)
    apartment_address = models.CharField(max_length=100)
    postal_code = models.CharField(max_length=20, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

