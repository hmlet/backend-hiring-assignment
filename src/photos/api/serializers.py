from django.contrib.auth.models import User
from django.core.files.images import get_image_dimensions
from django.conf import settings
from photos.models import Photo
from rest_framework.serializers import (
		ModelSerializer,
		ValidationError
	)



class UserSerializer(ModelSerializer):
	class Meta:
		model = User
		fields = [
			'id',
			'username'
		]


class PhotoSerializer(ModelSerializer):
	user = UserSerializer(read_only=True)
	class Meta:
		model = Photo
		fields = [
			'user',
			'image',
			'caption',
			'is_draft',
			'published_date'
		]

	def validate_image(self,data):
		image_width,image_height = get_image_dimensions(data)
		if image_width > settings.MAX_IMAGE_WIDTH:
			raise ValidationError("Max image width allowed is 1000")
		if image_height > settings.MAX_IMAGE_HEIGHT:
			raise ValidationError("Max image height allowed is 1000")
		if data.size > settings.MAX_IMAGE_SIZE:
			raise ValidationError("Image size can not exceed 2 megabyte")


#We can also make a serializer field in our serializer
#defined above, make one a write only and the other one
#as a read only
class CaptionEditSerializer(ModelSerializer):
	class Meta:
		model = Photo
		fields = ['caption']