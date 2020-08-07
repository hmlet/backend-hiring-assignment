from django.test import TestCase

# Create your tests here.
from rest_framework.test import APITestCase
from io import BytesIO
from django.core.files import File
from PIL import Image
from django.contrib.auth.hashers import make_password
from django.test import override_settings
from photos.models import Photo
from photos.api.serializers import PhotoSerializer
from django.urls import reverse
from rest_framework import status
from django.core.files.uploadedfile import SimpleUploadedFile
from datetime import timedelta
from django.contrib.auth.models import User

import tempfile
import json
import datetime

class PhotoListAllTest(APITestCase):


	def setUp(self):
		self.test_user = User.objects.create(username="test",password=make_password("test123"))

		self.test_user_creds = {
			"username":"test",
			"password":"test123"
		}

		self.user_image = self.generate_temp_image('test_image.png',100,100)


		self.test_unique_user = User.objects.create(username="uniqueuser", password=make_password("test123"))
		
		self.test_photo = Photo.objects.create(image = self.user_image,captions="Test Caption",user=self.test_user)
		self.test_photo.publishing_date ='2020-08-01'
		self.test_photo.save()


		self.draft_photo = Photo.objects.create(image = self.user_image,captions="Test Caption",user=self.test_user,is_draft=True)

		self.test_photo_two = Photo.objects.create(image = self.user_image,captions="Test Caption 2",user=self.test_user)
		self.test_photo_two.publishing_date ='2020-08-05'
		self.test_photo_two.save()

		self.test_photo_unique_user = Photo.objects.create(image = self.user_image,captions="Test Caption",user=self.test_unique_user)

	def generate_temp_image(self,name,width,height):
		image_file = BytesIO()
		image = Image.new('RGB', size=(100, 100),color='red')
		image.save(image_file, 'png')
		image_file.seek(0)
		return File(image_file, name=name)


	def get_test_server(self):
		return "http://testserver"

	def get_user_access_token(self):
		url = reverse('token_obtain_pair')
		user = self.test_user
		user.is_active=True
		user.save()
		response = self.client.post(url, self.test_user_creds, format='json')
		jwt_access_token = response.data['access']
		return jwt_access_token


	def test_all_photos_list(self):
		response = self.client.get(
			reverse('photo_list'),format='json')
		serializer = PhotoSerializer(Photo.objects.all(),many=True)			
		self.assertEqual(response.data[0]['user']['id'],serializer.data[0]['user']['id'])
		self.assertEqual(response.data[0]['user']['username'],serializer.data[0]['user']['username'])
		self.assertEqual(response.data[0]['image'],self.get_test_server()+serializer.data[0]['image'])
		self.assertEqual(response.data[0]['captions'],serializer.data[0]['captions'])
		self.assertEqual(len(response.data),len(serializer.data))
		self.assertEqual(response.status_code,status.HTTP_200_OK)

	def test_photos_list_ascending_order(self):
		response = self.client.get("/api/photos/all/?ordering=published_date")
		serializer = PhotoSerializer(Photo.objects.all(),many=True)
		photos = Photo.objects.all().order_by('published_date')
		self.assertEqual(response.data[0]['published_date'],photos[0].published_date.strftime('%Y-%m-%d'))
		self.assertEqual(response.data[1]['published_date'],photos[1].published_date.strftime('%Y-%m-%d'))
		self.assertEqual(response.status_code,status.HTTP_200_OK)
		

	def test_photos_list_descending_order(self):
		response = self.client.get("/api/photos/all/?ordering=-published_date")
		photos = Photo.objects.all().order_by('-published_date')
		self.assertEqual(response.data[0]['published_date'],photos[0].published_date.strftime('%Y-%m-%d'))
		self.assertEqual(response.data[1]['published_date'],photos[1].published_date.strftime('%Y-%m-%d'))
		self.assertEqual(response.status_code,status.HTTP_200_OK)
		
	def test_photos_list_search_user(self):
		response = self.client.get("/api/photos/all/?search=uniqueuser")
		photos = Photo.objects.filter(user__username = "uniqueuser")
		serializer = PhotoSerializer(photos,many=True)
		self.assertEqual(response.data[0]['user']['id'],serializer.data[0]['user']['id'])
		self.assertEqual(response.data[0]['user']['username'],serializer.data[0]['user']['username'])
		self.assertEqual(response.status_code,status.HTTP_200_OK)
		self.assertEqual(len(response.data),len(serializer.data))

	def test_photos_list_search_nonexisten_user(self):
		response   = self.client.get("/api/photos/all/?search=nonexistent")
		photos     = Photo.objects.filter(user__username = "nonexistent")
		serializer = PhotoSerializer(photos,many=True)
		self.assertEqual(response.data,serializer.data)
		self.assertEqual(response.status_code,status.HTTP_200_OK)
		self.assertEqual(len(response.data),len(serializer.data))








class UserDraftAndPhotoListTest(APITestCase):

	def setUp(self):
		self.test_user = User.objects.create(username="test",password=make_password("test123"))

		self.test_user_creds = {
			"username":"test",
			"password":"test123"
		}

		self.user_image = self.generate_temp_image('test_image.png',100,100)


		self.test_unique_user = User.objects.create(username="uniqueuser", password=make_password("test123"))
		
		self.test_photo = Photo.objects.create(image = self.user_image,captions="Test Caption",user=self.test_user)



		self.draft_photo = Photo.objects.create(image = self.user_image,captions="Test Caption",user=self.test_user,is_draft=True)

		self.test_photo_two = Photo.objects.create(image = self.user_image,captions="Test Caption 2",user=self.test_user)


		self.test_photo_unique_user = Photo.objects.create(image = self.user_image,captions="Test Caption",user=self.test_unique_user)




	def generate_temp_image(self,name,width,height):
		image_file = BytesIO()
		image = Image.new('RGB', size=(100, 100),color='red')
		image.save(image_file, 'png')
		image_file.seek(0)
		return File(image_file, name=name)

	def get_user_access_token(self):
		url = reverse('token_obtain_pair')
		user = self.test_user
		user.is_active=True
		user.save()
		response = self.client.post(url, self.test_user_creds, format='json')
		jwt_access_token = response.data['access']
		return jwt_access_token


	def test_auth_user_photo_list_unauthorized(self):
		response = self.client.get(reverse('user_photo_list'),format='json')
		self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

	def test_auth_user_photo_list_authorized(self):
		auth_token = 'JWT '+self.get_user_access_token()
		self.client.credentials(HTTP_AUTHORIZATION=auth_token)
		qs = Photo.objects.filter(user=self.test_user,is_draft=False)
		serializer = PhotoSerializer(qs,many=True)	
		response = self.client.get(reverse('user_photo_list'),format='json')
		self.assertEqual(response.data[0]['user']['username'], qs[0].user.username)
		self.assertEqual(response.data[0]['captions'], qs[0].captions)
		self.assertEqual(response.status_code, status.HTTP_200_OK)
		self.assertEqual(len(response.data),len(serializer.data))


	def test_auth_user_draft_photo_list_unauthorized(self):
		response = self.client.get(reverse('draft_photo_list'),format='json')
		self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

	def test_auth_user_draft_photo_list_authorized(self):
		auth_token = 'JWT '+self.get_user_access_token()
		self.client.credentials(HTTP_AUTHORIZATION=auth_token)
		qs = Photo.objects.filter(user=self.test_user,is_draft=True)
		serializer = PhotoSerializer(qs,many=True)	
		response = self.client.get(reverse('draft_photo_list'),format='json')
		self.assertEqual(response.data[0]['is_draft'], qs[0].is_draft)
		self.assertEqual(response.data[0]['captions'], qs[0].captions)
		self.assertEqual(response.status_code, status.HTTP_200_OK)
		self.assertEqual(len(response.data),len(serializer.data))



class CreatePhotoTestCases(APITestCase):
	def setUp(self):
		self.test_user = User.objects.create(username="test",password=make_password("test123"))

		self.test_user_creds = {
			"username":"test",
			"password":"test123"
		}

		self.test_file = self.generate_temp_image('ab.jpg',100,100)


	def generate_temp_image(self,name,width,height):
		image_file = BytesIO()
		image = Image.new('RGB', size=(100, 100),color='red')
		image.save(image_file, 'png')
		image_file.seek(0)
		return File(image_file, name=name)


	def get_user_access_token(self):
		url = reverse('token_obtain_pair')
		user = self.test_user
		user.is_active=True
		user.save()
		response = self.client.post(url, self.test_user_creds, format='json')
		jwt_access_token = response.data['access']
		return jwt_access_token

	def test_create_photo(self):
		auth_token = 'JWT '+self.get_user_access_token()
		self.client.credentials(HTTP_AUTHORIZATION=auth_token)
		response = self.client.post(
			reverse('create_photo'),
			data={"image":self.test_file,"captions":"test caption"},
			format = 'multipart'
		)
		self.assertEqual(response.status_code, status.HTTP_201_CREATED)

	def test_create_photo(self):
		auth_token = 'JWT '+self.get_user_access_token()
		self.client.credentials(HTTP_AUTHORIZATION=auth_token)
		response = self.client.post(
			reverse('create_photo'),
			data={"image":self.test_file,"captions":"test caption"},
			format = 'multipart'
		)
		self.assertEqual(response.data['captions'], 'test caption')
		self.assertEqual(response.status_code, status.HTTP_201_CREATED)
	def test_create_invalid_file(self):
		auth_token = 'JWT '+self.get_user_access_token()
		self.client.credentials(HTTP_AUTHORIZATION=auth_token)
		image = Image.new('RGB', (100, 100))
		tmp_file = tempfile.NamedTemporaryFile(suffix='.pdf')
		image.save(tmp_file)
		with open(tmp_file.name, 'rb') as data:
			response = self.client.post(
				reverse('create_photo'),
				data={"image":data,"captions":"test caption"},
				format = 'multipart'
			)
		
			self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

	def test_create_draft_photo(self):
		auth_token = 'JWT '+self.get_user_access_token()
		self.client.credentials(HTTP_AUTHORIZATION=auth_token)
		response = self.client.post(
			reverse('create_photo'),
			data={"image":self.test_file,"captions":"test caption","is_draft":True},
			format = 'multipart'
		)
		self.assertEqual(response.data['is_draft'], True)
		self.assertEqual(response.status_code, status.HTTP_201_CREATED)






class UpdatePhotoCaptionsTestCases(APITestCase):

	def setUp(self):
		self.test_user  = User.objects.create(username="test",password=make_password("test123"))
		self.test_file = self.generate_temp_image('ab.jpg',100,100)
		self.test_photo = Photo.objects.create(image =self.test_file,captions="Test Caption",user=self.test_user)

		self.test_user_two = User.objects.create(username="test2",password=make_password("test12345"))

		self.updated_captions = {
			"captions": "Edited" 
		}

		self.test_user_creds = {
			"username":"test",
			"password":"test123"
		}

		self.test_two_user_creds = {
			"username":"test2",
			"password":"test12345"
		}


	def generate_temp_image(self,name,width,height):
		image_file = BytesIO()
		image = Image.new('RGB', size=(100, 100),color='red')
		image.save(image_file, 'png')
		image_file.seek(0)
		return File(image_file, name=name)



	def get_user_access_token(self,test_creds_data):
		url = reverse('token_obtain_pair')
		user = self.test_user
		user.is_active=True
		user.save()
		response = self.client.post(url, test_creds_data, format='json')
		jwt_access_token = response.data['access']
		return jwt_access_token

	def test_valid_update_captions(self):
		auth_token = 'JWT '+self.get_user_access_token(self.test_user_creds)
		self.client.credentials(HTTP_AUTHORIZATION=auth_token)
		response = self.client.put(
			reverse('update_photo_captions',kwargs={'pk': self.test_photo.id}),
			data= self.updated_captions ,
		)
		
		self.assertEqual(response.status_code, status.HTTP_200_OK)

	def test_update_captions_with_no_data(self):
		auth_token = 'JWT '+self.get_user_access_token(self.test_user_creds)
		self.client.credentials(HTTP_AUTHORIZATION=auth_token)
		response = self.client.put(
			reverse('update_photo_captions',kwargs={'pk': self.test_photo.id}),
		)
		self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

	def test_update_captions_authenticated_unauthorized_user(self):
		auth_token = 'JWT '+self.get_user_access_token(self.test_two_user_creds)
		self.client.credentials(HTTP_AUTHORIZATION=auth_token)
		response = self.client.put(
			reverse('update_photo_captions',kwargs={'pk': self.test_photo.id}),
			data= self.updated_captions,
		)
		self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


	def test_update_captions_unauthenticated_user(self):
		response = self.client.put(
			reverse('update_photo_captions',kwargs={'pk': self.test_photo.id}),
			data= self.updated_captions,
		)
		self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)




class DeletePhotoTestCases(APITestCase):

	def setUp(self):
		self.test_user  = User.objects.create(username="test",password=make_password("test123"))
		self.test_file = self.generate_temp_image('ab.jpg',100,100)
		self.test_photo = Photo.objects.create(image =self.test_file,captions="Test Caption",user=self.test_user)
		

		self.test_user_two = User.objects.create(username="test2",password=make_password("test12345"))

		self.updated_captions = {
			"captions": "Edited" 
		}

		self.test_user_creds = {
			"username":"test",
			"password":"test123"
		}

		self.test_two_user_creds = {
			"username":"test2",
			"password":"test12345"
		}	

	def generate_temp_image(self,name,width,height):
		image_file = BytesIO()
		image = Image.new('RGB', size=(100, 100),color='red')
		image.save(image_file, 'png')
		image_file.seek(0)
		return File(image_file, name=name)


	def get_user_access_token(self,test_creds_data):
		url = reverse('token_obtain_pair')
		user = self.test_user
		user.is_active=True
		user.save()
		response = self.client.post(url, test_creds_data, format='json')
		jwt_access_token = response.data['access']
		return jwt_access_token


	def test_delete_photo_authenticated_user(self):
		auth_token = 'JWT '+self.get_user_access_token(self.test_user_creds)
		self.client.credentials(HTTP_AUTHORIZATION=auth_token)
		response = self.client.delete(
			reverse('delete_photo',kwargs={'pk': self.test_photo.id}),
		)
		self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)


	def test_delete_photo_unauthenticated_user(self):
		response = self.client.delete(
			reverse('delete_photo',kwargs={'pk': self.test_photo.id}),
		)
		self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)



	def test_delete_photo_authenticated_unauthorized_user(self):
		auth_token = 'JWT '+self.get_user_access_token(self.test_two_user_creds)
		self.client.credentials(HTTP_AUTHORIZATION=auth_token)
		response = self.client.delete(
			reverse('delete_photo',kwargs={'pk': self.test_photo.id}),
		)
		self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)



	def test_delete_photo_noexistent_photo_object(self):
		auth_token = 'JWT '+self.get_user_access_token(self.test_two_user_creds)
		self.client.credentials(HTTP_AUTHORIZATION=auth_token)
		response = self.client.delete(
			reverse('delete_photo',kwargs={'pk': 100}),
		)
		self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)





