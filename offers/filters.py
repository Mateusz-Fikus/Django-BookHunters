import django_filters
from .models import offer
from django_filters import NumberFilter, CharFilter

class OfferFilter(django_filters.FilterSet):
    start_price = NumberFilter(field_name="price", lookup_expr='gte')
    end_price = NumberFilter(field_name="price", lookup_expr='lte')
    title = CharFilter(field_name='title', lookup_expr='icontains')
    class Meta:
        model = offer
        fields = ['title', 'genre']