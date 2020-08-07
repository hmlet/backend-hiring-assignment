from django.urls import path

from .views import (
	PhotosListAPIView,
	UserPhotosListApiView,
	UserDraftPhotosListApiView,
	PhotoCreateAPIView,
	UpdatePhotoCaptionsAPIView,
	DestroyPhotoAPIView,
)


urlpatterns = [
    path("all/", PhotosListAPIView.as_view(),name='photo_list'),
    path("user/", UserPhotosListApiView.as_view(),name='user_photo_list'),
    path("user/drafts/",  UserDraftPhotosListApiView.as_view(), name='draft_photo_list'),
    path("create/", PhotoCreateAPIView.as_view(),name="create_photo"),
    path("update/<int:pk>/", UpdatePhotoCaptionsAPIView.as_view(),name="update_photo_caption"),
    path("delete/<int:pk>/", DestroyPhotoAPIView.as_view(),name="delete_photo"),
]