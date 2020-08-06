from django.urls import path

from .views import (
	PhotosListAPIView,
	UserPhotosListApiView
)


urlpatterns = [
    path("all/", PhotosListAPIView.as_view(),name='photo_list'),
    path("me/", UserPhotosListApiView.as_view(),name='user_photo_list'),
]