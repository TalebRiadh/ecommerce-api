
from django.contrib import admin
from django.urls import path, include, re_path
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from dj_rest_auth.registration.views import VerifyEmailView, ResendEmailVerificationView
from django.views.generic import TemplateView
from django.conf import settings
from django.conf.urls.static import static
from dj_rest_auth.views import PasswordResetView, PasswordResetConfirmView, PasswordChangeView, LogoutView
from products.views import PublisherDocumentView

schema_view = get_schema_view(
   openapi.Info(
      title="E-commerce API",
      default_version='v1',
      description="This is a REST API for a E-commerce service",
      terms_of_service="https://www.google.com/policies/terms/",
      contact=openapi.Contact(email="contact@snippets.local"),
      license=openapi.License(name="BSD License"),
   ),
   public=True,
   permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('user/',include('authentication.urls', namespace='authentication')),
    path('products/', include('products.urls', namespace='products')),
    path('orders/',include('orders.urls')),
    path('payment/', include('payment.urls', namespace='payment')),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),



    path('resend-email/', ResendEmailVerificationView.as_view(),
         name="rest_resend_email"),
    re_path(
        r'^account-confirm-email/(?P<key>[-:\w]+)/$', VerifyEmailView.as_view(),
        name='account_confirm_email',
    ),
    path(
        'account-email-verification-sent/', TemplateView.as_view(),
        name='account_email_verification_sent',
    ),
    path('search/' , PublisherDocumentView.as_view({'get': 'list'})),



    path('password/reset/', PasswordResetView.as_view(),
         name='rest_password_reset'),
    path('password/reset/confirm/<str:uidb64>/<str:token>',
         PasswordResetConfirmView.as_view(), name='password_reset_confirm'),

    path('password/change/', PasswordChangeView.as_view(),
         name='rest_password_change'),

    path('logout/', LogoutView.as_view(), name='rest_logout'),

    path('swagger<format>.json|.yaml/', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    path('docs/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
if settings.DEBUG:
     import debug_toolbar
     urlpatterns = [
          path('__debug__/', include(debug_toolbar.urls)),
     ] + urlpatterns