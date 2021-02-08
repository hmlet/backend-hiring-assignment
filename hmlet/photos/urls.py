from django.urls import path
from . import views
from .views import PostListView, PostDetailView, PostCreateView, PostUpdateView, PostDeleteView, UserPostListView, TagListView

# from django.urls import path
# from myapi.core import views
# from django.conf.urls import patterns, include, url

urlpatterns = [
    # path('home/', views.home, name='photos-home'),
    path('', PostListView.as_view(), name='photos-home'),
    path('user/<str:username>', UserPostListView.as_view(), name='user-posts'),
    path('post/<int:pk>/', PostDetailView.as_view(), name='post-detail'),
    path('post/new/', PostCreateView.as_view(), name='post-create'),
    path('post/<int:pk>/update', PostUpdateView.as_view(), name='post-update'),
    path('post/<int:pk>/delete', PostDeleteView.as_view(), name='post-delete'),
    path('about/', views.about, name='photos-about'),

    path('tags/<slug:tag_slug>/',TagListView.as_view(),name='caption_by_tags'),

    path('hello/', views.HelloView.as_view(), name='hello'),

]