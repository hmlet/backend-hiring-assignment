from rest_framework.generics import ListAPIView
from .serializers import PhotoSerializer
from photos.models import Photo

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