from rest_framework import viewsets, filters
from rest_framework.pagination import PageNumberPagination
from .models import Customer
from .serializers import CustomerSerializer

class StandardResultsSetPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 100

class CustomerViewSet(viewsets.ModelViewSet):
    queryset = Customer.objects.filter(is_active=True).order_by('-created_at')
    serializer_class = CustomerSerializer
    pagination_class = StandardResultsSetPagination
    filter_backends = [filters.SearchFilter]
    search_fields = ['phone']

    def perform_destroy(self, instance):
        instance.delete()
