from django.shortcuts import render
from django.views import View
from .models import Post


class IndexView(View):
    def get(self,request):
        posts = Post.objects.all()
        return render(request,"home/home.html",{
            "posts":posts
        })

