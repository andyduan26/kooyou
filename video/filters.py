import django_filters

from .models import Video


class VideoFilter(django_filters.FilterSet):
    channel = django_filters.CharFilter(field_name="category__channel")
    category = django_filters.NumberFilter(field_name="category_id")
    member_only = django_filters.BooleanFilter()
    keyword = django_filters.CharFilter(field_name="title", lookup_expr="icontains")

    class Meta:
        model = Video
        fields = ["channel", "category", "member_only", "keyword"]
