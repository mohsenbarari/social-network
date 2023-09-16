from django.shortcuts import render

from django.views import View


class IndexView(View):
    def get(self,request):
        contents = "Hi there, welcome to index page"
        return render(request,"home/home.html",{
            "contents":contents
        })

