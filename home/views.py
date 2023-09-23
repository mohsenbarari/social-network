from typing import Any
from django import http
from django.shortcuts import render,redirect
from django.views import View
from .models import Post
from django.contrib import messages
from .forms import PostUpdateForm
from django.utils.text import slugify


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
    

class PostDeleteView(View):

    def get(self,request,post_id):
        post = Post.objects.get(pk=post_id)
        if request.user.id == post.user.id:
            post.delete()
            messages.success(request,"your post deleted")
        else:
            messages.error(request,"you don't delete this post")
        return redirect('home:index')
    

class PostUpdateView(View):
    form_class = PostUpdateForm
    template_page = "home/update.html"

    def setup(self, request, *args, **kwargs):
        self.post_instance = Post.objects.get(pk=kwargs["post_id"])
        return super().setup(request, *args, **kwargs)
    
    def dispatch(self, request, *args, **kwargs):
        post = self.post_instance
        if post.user.id != request.user.id:
            messages.error(request,"you don't permmsion this post","danger")
            return redirect("home:post-detail",post.id,post.slug)
        return super().dispatch(request, *args, **kwargs)
    

    def get(self,request,post_id):
        post = self.post_instance
        form = self.form_class(instance=post)
        return render(request,self.template_page,{
            "form":form,
        })
    def post(self,request,post_id):
        post = self.post_instance
        form = self.form_class(request.POST,instance=post)
        if form.is_valid():
            cd = form.cleaned_data
            new_post = form.save(commit=False)
            new_post.slug = slugify(cd["title"])
            new_post.save()
            messages.success(request,"update post is ok","success")
            return redirect("home:post-detail" ,post.id, post.slug)


