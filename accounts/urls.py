from django.urls import path
from . import views


app_name = "accounts"
urlpatterns = [
    path("register/",views.UserRgisterView.as_view(),name="user-register")
]