from django.shortcuts import render,redirect
from django.views import View
from .models import Post
from django.contrib import messages
from .forms import PostUpdateForm,PostCreateForm
from django.utils.text import slugify
from django.contrib.auth.mixins import LoginRequiredMixin



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
    

class PostDeleteView(LoginRequiredMixin,View):

    def get(self,request,post_id):
        post = Post.objects.get(pk=post_id)
        if request.user.id == post.user.id:
            post.delete()
            messages.success(request,"your post deleted")
        else:
            messages.error(request,"you don't delete this post")
        return redirect('home:index')
    

class PostUpdateView(LoginRequiredMixin,View):
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
        

class PostCreateView(LoginRequiredMixin,View):
    form_class = PostCreateForm
    template_page = "home/create.html"

    def get(self,request):
        form = self.form_class()
        return render(request,self.template_page,{
            "form":form,
        })

    def post(self,request):
        form = self.form_class(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            new_post = form.save(commit=False)
            new_post.user = request.user
            new_post.title = cd["title"]
            new_post.body = cd["body"]
            new_post.slug = slugify(cd["title"])
            new_post.save()
            messages.success(request,"your poast creted")
            return redirect("home:post-detail",new_post.id,new_post.slug)








