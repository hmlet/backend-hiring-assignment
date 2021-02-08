from django.contrib import admin

# Register your models here.
from .models import photos, PostImage

admin.site.register(photos)



class PostImageAdmin(admin.StackedInline):
    model = PostImage
 
# @admin.register(photos)
class PostAdmin(admin.ModelAdmin):
    inlines = [PostImageAdmin]
 
    class Meta:
       model = photos
 
@admin.register(PostImage)
class PostImageAdmin(admin.ModelAdmin):
    pass