from django.urls import path
from . import views


app_name = "accounts"
urlpatterns = [
    path("register/",views.UserRgisterView.as_view(),name="user-register"),
    path("login/",views.UserLoginView.as_view(),name="user-login"),
    path("logout/",views.UserLogoutView.as_view(),name="user-logout"),
    path("profile/<int:user_id>/",views.UserProfileView.as_view(),name="user-profile"),



    
]