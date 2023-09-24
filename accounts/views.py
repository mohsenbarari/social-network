from typing import Any
from django import http
from django.shortcuts import render,redirect
from django.contrib import messages
from django.contrib.auth import login , authenticate , logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import View
from django.contrib.auth.models import User
from .forms import UserRegisterForm,UserLoginForm
from home.models import Post


class UserRgisterView(View):
    form_class = UserRegisterForm
    template_page = "accounts/register.html"
    
    def setup(self,request,*args,**kwargs):
        self.next = request.GET.get("next")
        return super().setup(request,*args,**kwargs)

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect("home:index")
        return super().dispatch(request, *args, **kwargs)
    

    def get(self,request):
        form = self.form_class
        return render(request,self.template_page,{
            "form":form
        })
    
    def post(self,request):
        form = self.form_class(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            User.objects.create_user(cd["username"],cd["email"],cd["password1"])
            messages.success(request,f"Hi {cd['username']}! you'r registered","success")
            user = authenticate(request,username=cd["username"],password=cd ["password1"])
            login(request,user)
            if self.next:
                return redirect(self.next)
            return redirect("home:index")
        else:
            return render(request,self.template_page,{
            "form":form})


class UserLoginView(View):
    form_class = UserLoginForm
    template_page = "accounts/login.html"

    def setup(self, request, *args, **kwargs):
        self.next = request.GET.get("next")
        return super().setup(request, *args, **kwargs)

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect("home:index")
        return super().dispatch(request, *args, **kwargs)

    def get(self,request):
        form = self.form_class()
        return render(request,self.template_page,{
            "form":form
        })
        

    def post(self,request):
        form = self.form_class(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(request,username=cd["username"],password=cd ["password"])
            if user is not None:
                login(request,user)
                messages.success(request,f"Hi {request.user}! your welcome","success")
                if self.next:
                    return redirect(self.next)
                
                return redirect("home:index")
            messages.error(request,"username or password is wrong","danger")
            return redirect("accounts:user-login")


class UserLogoutView(LoginRequiredMixin,View):
    def get(self,request):
        logout(request)
        messages.success(request,"you loged out","success")
        return redirect("home:index")
    

class UserProfileView(LoginRequiredMixin,View):
    def get(self,request,user_id):
        user = User.objects.get(pk=user_id)
        posts = Post.objects.filter(user=user)
        return render(request,"accounts/profile.html",{
            "user":user,
            "posts":posts
        })
