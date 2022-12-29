from rest_framework import permissions, viewsets

from .documents import *
from .models import Product, ProductCategory
from .permissions import IsSellerOrAdmin
from .serializers import (
        NewsDocumentSerializer,
            ProductCategoryReadSerializer, 
            ProductReadSerializer,
            CreateProductSerializer)
from django_elasticsearch_dsl_drf.filter_backends import (
    FilteringFilterBackend,
    CompoundSearchFilterBackend
)
from django_elasticsearch_dsl_drf.viewsets import DocumentViewSet
from django_elasticsearch_dsl_drf.filter_backends import (
    FilteringFilterBackend,
    OrderingFilterBackend,
)

# Create your views here.

class ProductCategoryViewSet(viewsets.ReadOnlyModelViewSet):
    """
    List and Retrieve product categories
    """
    queryset = ProductCategory.objects.all()
    serializer_class = ProductCategoryReadSerializer
    permission_classes = (permissions.AllowAny,)


class ProductViewSet(viewsets.ModelViewSet):
    """
    CRUD products
    """
    queryset = Product.objects.all()

    def get_serializer_class(self):
        if self.action in ('create', 'update', 'partial_update', 'destroy'):
            return CreateProductSerializer
        return ProductReadSerializer

    def get_permissions(self):
        if self.action in ('create', ):
            self.permission_classes = (permissions.IsAuthenticated,)
        elif self.action in ('update', 'partial_update', 'destroy'):
            self.permission_classes = (IsSellerOrAdmin,)
        else:
            self.permission_classes =(permissions.AllowAny,)
        
        return super().get_permissions()


class PublisherDocumentView(DocumentViewSet):
    document = ProductDocument
    serializer_class = NewsDocumentSerializer
    lookup_field = 'first_name'
    fielddata=True
    filter_backends = [
        FilteringFilterBackend,
        OrderingFilterBackend,
        CompoundSearchFilterBackend,
    ]
   
    search_fields = (
        'name',
        'desc',
    )
    multi_match_search_fields = (
       'name',
        'desc',
    )
    filter_fields = {
       'name' : 'name',
        'desc' : 'desc',
    }
    ordering_fields = {
        'id': None,
    }
    ordering = ( 'id'  ,)
        