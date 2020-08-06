from rest_framework.serializers import (
		ModelSerializer,
		ValidationError
	)

from photos.models import Photo
from django.contrib.auth.models import User


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
			'captions',
			'is_draft',
			'published_date'
		]


#We can also make a serializer field in our serializer
#defined above, make one a write only and the other one
#as a read only
class CaptionEditSerializer(ModelSerializer):
	class Meta:
		model = Photo
		fields = ['captions']