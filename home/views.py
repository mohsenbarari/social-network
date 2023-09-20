from django.shortcuts import render,redirect
from django.views import View
from .models import Post
from django.contrib import messages


class IndexView(View):
    def get(self,request):
        posts = Post.objects.all()
        return render(request,"home/home.html",{
            "posts":posts
        })

class PostDetailView(View):
    def get(self,request,post_id,post_slug):
        post = Post.objects.get(pk=post_id,slug=post_slug)
        return render (request,"home/detail.html",{
            "post":post,
            
        })
    

class DeletePostView(View):

    def get(self,request,post_id):
        post = Post.objects.get(pk=post_id)
        if request.user.id == post.user.id:
            post.delete()
            messages.success(request,"your post deleted")
        else:
            messages.error(request,"you don't delete this post")
        return redirect('home:index')