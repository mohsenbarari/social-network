from django.shortcuts import render,redirect
from django.contrib import messages
from django.views import View
from django.contrib.auth.models import User
from .forms import UserRegisterForm


class UserRgisterView(View):
    form_class = UserRegisterForm
    template_page = "accounts/register.html"

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
            return redirect("home:index")
        else:
            return render(request,self.template_page,{
            "form":form})


