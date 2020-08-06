from photos.models import Photo

from rest_framework.generics import (
	ListAPIView,
	CreateAPIView,
	UpdateAPIView,
	DestroyAPIView
)

from .serializers import (
	PhotoSerializer,
	CaptionEditSerializer
)

class PhotosListAPIView(ListAPIView):
	queryset = Photo.objects.all()
	serializer_class = PhotoSerializer



class UserPhotosListApiView(ListAPIView):
    queryset = Photo.objects.all()
    serializer_class = PhotoSerializer
   
    def get_queryset(self):
        user = self.request.user
        qs = Photo.objects.filter(user=user,is_draft=False)
        return qs

class UserDraftPhotosListApiView(ListAPIView):
    queryset = Photo.objects.all()
    serializer_class = PhotoSerializer

    def get_queryset(self):
        user = self.request.user
        qs = Photo.objects.filter(user=user,is_draft=True)
        return qs


class PhotoCreateAPIView(CreateAPIView):
	queryset = Photo.objects.all()
	serializer_class = PhotoSerializer

	def perform_create(self,serializer):
		serializer.save(user=self.request.user)


class UpdatePhotoCaptionsAPIView(UpdateAPIView):
	queryset = Photo.objects.all()
	serializer_class = CaptionEditSerializer
	lookup_field  = 'pk'


class DestroyPhotoAPIView(DestroyAPIView):
    queryset = Photo.objects.all()
    serializer_class = PhotoSerializer
    lookup_field = 'pk'





