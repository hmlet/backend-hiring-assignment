from django.shortcuts import render, get_object_or_404
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

class PostListView(ListView):
    model = photos
    template_name = 'photos/home.html'
    context_object_name = 'posts'
    # ordering = ['published_date']
    paginate_by = 2
    ordering =['-is_draft']

class TagListView(ListView):
    model = photos
    template_name = 'photos/photos_list.html'
    context_object_name = 'posts'
    # ordering = ['published_date']
    paginate_by = 2
    ordering =['-is_draft']

    def get_queryset(self):
        tags = get_object_or_404(User, username=self.kwargs.get('tags'))
        return photos.objects.filter(tags_slug = tags)

        # return photos.objects.filter(author=user)

    
     

class UserPostListView(ListView):
    model = photos
    template_name = 'photos/photos_list.html'
    context_object_name = 'posts'
    # ordering = ['published_date']
    paginate_by = 2

    def get_queryset(self):
        user = get_object_or_404(User, username=self.kwargs.get('username'))
        return photos.objects.filter(author=user).order_by('published_date').order_by('is_draft')


class PostDetailView(DetailView):
    model = photos
    
class PostCreateView(LoginRequiredMixin,CreateView):
    model = photos
    fields= ['image','caption','is_draft','tags']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

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
