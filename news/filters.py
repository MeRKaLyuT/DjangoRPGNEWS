from django_filters import FilterSet
from .models import Post, Comments

class CommentFilter(FilterSet):
    class Meta:
        model = Comments
        fields = {
            'connect_post': ['exact']
        }

