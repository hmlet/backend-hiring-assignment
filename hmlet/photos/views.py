from django.shortcuts import render, get_object_or_404
import base64
import re
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.models import User
from django.http import HttpResponse
from .models import photos, PostImage
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView 

from taggit.models import Tag

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

def home(request):
    context= {
        'posts':photos.objects.all()
    }
    return render(request,'photos/home.html',context)

# Create your views here.

# FOR POST LIST VIEW 
# IN THIS SORTING CAN BE DONE BY PUBLISHED_DATE, IS_DRAFT. I DIDN'T INTEGRATE  ALL OF THESE INTO INTEGRATE FRONTEND. BUT THE QUERY CAN BE MODIFIED HERE
# LIKE ordering=['-published_date'], ['published_date'], ['is_draft'], ['-is_draft'] 
# THIS CAN BE FOLOWED BY BELOW ALL THE FUNCTIONS 
class PostListView(ListView):
    model = photos
    template_name = 'photos/home.html'
    context_object_name = 'posts'
    ordering = ['-published_date']
    paginate_by = 2
    ordering =['-is_draft']

#FOR TAGS LIST VIEW
class TagListView(ListView):
    model = photos  
    template_name = 'photos/tags_list.html'
    context_object_name = 'posts'
    ordering = ['-published_date']
    paginate_by = 2
    # ordering =['-is_draft']

    def get_queryset(self):
        # tag = get_object_or_404(User, tags=self.kwargs.get('tags'))
        return photos.objects.filter(tags = self.kwargs.get('tags'))

        # return photos.objects.filter(tags=tags)

    
     
#FOR PHOTOS ACCORDING TO THE USER VIEW 
class UserPostListView(ListView):
    model = photos
    template_name = 'photos/photos_list.html'
    context_object_name = 'posts'
    ordering = ['-published_date']
    paginate_by = 2

    def get_queryset(self):
        user = get_object_or_404(User, username=self.kwargs.get('username'))
        return photos.objects.filter(author=user).order_by('published_date').order_by('-is_draft')

#FOR SPECIFIC PHOTO POST VIEW IT SHOWS ONLY ONE WHICH IS REQUIRED 
class PostDetailView(DetailView):
    model = photos


# FOR CREATING A NEW POST
class PostCreateView(LoginRequiredMixin,CreateView):
    model = photos
    fields= ['image','caption','is_draft','tags']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

#FOR UPDATING A PHOTO POST (PHOTO,CAPTION,DRAFT,TAGS) DONE BY LOGGED IN SPECIFIC USER OONLY
class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = photos
    fields= ['image','caption','is_draft','tags']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author :
            return True
        return False


#FOR DELETING A PHOTO POST (PHOTO,CAPTION,DRAFT,TAGS) DONE BY LOGGED IN SPECIFIC USER OONLY
class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = photos
    success_url = '/'

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author :
            return True
        return False



def about(request):
    return render(request,'photos/about.html',{'title':'About'})


#FOR JWT AUTHENTICATION 
class HelloView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        content = {'message': 'Hello, World!'}
        return Response(content)


def blog_view(request):
    posts = photos.objects.all()
    return render(request, 'photos/home.html', {'posts':posts})
 
def detail_view(request, id):
    post = get_object_or_404(Post, id=id)
    photos = PostImage.objects.filter(post=post)
    return render(request, 'detail.html', {
        'post':post,
        'photos':photos
    })
