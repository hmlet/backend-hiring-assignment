from django.urls import path
from . import views
from .views import PostListView, PostDetailView, PostCreateView, PostUpdateView, PostDeleteView, UserPostListView, TagListView

# from django.urls import path
# from myapi.core import views
# from django.conf.urls import patterns, include, url

urlpatterns = [
    # path('home/', views.home, name='photos-home'),

    #Below path is for the List view Api 
    path('', PostListView.as_view(), name='photos-home'),

    #Below Path is for the User list. This is accessed by clicking the user(author)
    path('user/<str:username>', UserPostListView.as_view(), name='user-posts'),

    #Below Path is for the Details of the post specific one Photo Post with Number 
    path('post/<int:pk>/', PostDetailView.as_view(), name='post-detail'),

    #Below Path is for the Add photo 
    path('post/new/', PostCreateView.as_view(), name='post-create'),

    #Path for  Upadating a Photo/ Caption/ Draft/ Tags
    path('post/<int:pk>/update', PostUpdateView.as_view(), name='post-update'),

    #Path for Deleting 
    path('post/<int:pk>/delete', PostDeleteView.as_view(), name='post-delete'),

    #For Simply creating at starting of the project
    path('about/', views.about, name='photos-about'),

    #For Tags 
    path('tags/<slug:tag_slug>/',TagListView.as_view(),name='caption_by_tags'),

    #For JWT Authentication
    path('hello/', views.HelloView.as_view(), name='hello'),

]