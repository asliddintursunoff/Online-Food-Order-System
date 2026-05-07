import django_filters

from apps.products.models import Product


class CategoryFilter(django_filters.FilterSet):
    category = django_filters.CharFilter(
        field_name="category__name"
    )
    class Meta:
        model = Product
        fields = []