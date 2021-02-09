from django.db import models
from django.contrib.auth.models import User
from PIL import Image
from django.conf import settings
from django.urls import reverse
from datetime import datetime, date
from django.core.exceptions import ValidationError
from taggit.managers import TaggableManager

User = settings.AUTH_USER_MODEL

class photos(models.Model):
    author = models.ForeignKey(User,on_delete=models.CASCADE)
    image = models.ImageField(upload_to='photos_pics',width_field='image_width',height_field='image_height')
    image_width	= models.PositiveIntegerField(blank=True,null=True)
    image_height = models.PositiveIntegerField(blank=True,null=True)
    caption = models.CharField(max_length=250)
    is_draft = models.BooleanField(default=False)
    published_date = models.DateField(auto_now_add=True)
    tags = TaggableManager()


    # def __str__(self):
    #     return f'{self.user.username} photos'

    # FUNCTION WHICH IS USED TO SAVE THE PHOTO ACCORDING TO THE PREDEFIEND VALUES , 
    def save(self, *args, **kwargs):
        super(photos, self).save(*args, **kwargs)
        
        img = Image.open(self.image.path)
        
        if img.height > 400 or img.width >400:
            output_size = (400,400)
            img.thumbnail(output_size)
            img.save(self.image.path)
    
    # FUNCTION USED TO VALIDATE THE IMAGE SIZE 
    def validate_image(self, *args, **kwargs):
        image_width,image_height = get_image_dimensions(image)
        if image_width > settings.MAX_IMAGE_WIDTH:
            raise ValidationError("Max image width allowed is 1000")
        if image_height > settings.MAX_IMAGE_HEIGHT:
            raise ValidationError("Max image height allowed is 1000")
        if image.size > settings.MAX_IMAGE_SIZE:
            raise ValidationError("Image size can not exceed 2 megabyte")
        
    def get_absolute_url(self):
        return reverse('post-detail',kwargs={'pk':self.pk})

class PostImage(models.Model):
    post = models.ForeignKey(photos, default=None, on_delete=models.CASCADE)
    images = models.FileField(upload_to = 'images/')

    def __str__(self):
        return f'{self.images} PostImage'





