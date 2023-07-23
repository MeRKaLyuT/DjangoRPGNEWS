from django.urls import path
from .views import *
from django.contrib import admin
from django.conf.urls.static import static
from django.conf import settings
from django.conf.urls import include


urlpatterns = [
    path('', PostList.as_view(), name='news'),
    path('post/<int:pk>', PostDetail.as_view(), name='post'),
    path('create/', PostCreate.as_view(), name='post_create'),
    path('<int:pk>/edit/', PostEdit.as_view(), name='post_edit'),
    path('profile/', Profile, name='profile'),
    path('addcom', CommentCreateView.as_view(), name='comment_create'),
    path('usercomments/', user_comments, name="usercomments"),
    path('authorcomments/', author_comments, name='authorcomments'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

