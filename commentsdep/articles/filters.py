import django_filters
from django_filters import CharFilter
from .models import *


class ArticleFilter(django_filters.FilterSet):

    title_search = CharFilter(field_name='title', lookup_expr='icontains')

    class Meta:
        model = Article 
        fields = '__all__'
