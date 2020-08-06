from photos.models import Photo

from rest_framework.filters import OrderingFilter,SearchFilter

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

from rest_framework.permissions import IsAuthenticated

class PhotosListAPIView(ListAPIView):
	queryset = Photo.objects.all()
	serializer_class = PhotoSerializer
	filter_backends = [OrderingFilter,SearchFilter]
	ordering_fields = ['published_date']
	search_fields =   ['user__username']



class UserPhotosListApiView(ListAPIView):
	queryset = Photo.objects.all()
	serializer_class = PhotoSerializer
	permission_classes = [IsAuthenticated]

	def get_queryset(self):
		user = self.request.user
		qs = Photo.objects.filter(user=user,is_draft=False)
		return qs

#Can be merged with user photo list api view above
#by using query params and get the draft objects
#for the user who is requesting
class UserDraftPhotosListApiView(ListAPIView):
	queryset = Photo.objects.all()
	serializer_class = PhotoSerializer
	permission_classes = [IsAuthenticated]

	def get_queryset(self):
		user = self.request.user
		qs = Photo.objects.filter(user=user,is_draft=True)
		return qs


class PhotoCreateAPIView(CreateAPIView):
	queryset = Photo.objects.all()
	serializer_class = PhotoSerializer
	permission_classes = [IsAuthenticated]

	def perform_create(self,serializer):
		serializer.save(user=self.request.user)


class UpdatePhotoCaptionsAPIView(UpdateAPIView):
	queryset = Photo.objects.all()
	serializer_class = CaptionEditSerializer
	permission_classes = [IsAuthenticated]
	lookup_field  = 'pk'


class DestroyPhotoAPIView(DestroyAPIView):
	queryset = Photo.objects.all()
	serializer_class = PhotoSerializer
	permission_classes = [IsAuthenticated]
	lookup_field = 'pk'





