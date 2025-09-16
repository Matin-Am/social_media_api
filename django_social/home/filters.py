import django_filters
from .models import Post





class PostFilter(django_filters.FilterSet):
    created = django_filters.DateFilter(field_name="created", lookup_expr="exact")
    created_lte = django_filters.DateFilter(field_name="created",lookup_expr="lte")
    created_gte = django_filters.DateFilter(field_name="created",lookup_expr="gte")

    class Meta: 
        model = Post
        fields = {
            "user":['exact'],
        }