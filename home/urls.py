from django.urls import path
from . import views


app_name = "home"
urlpatterns = [
    path("index/",views.IndexView.as_view(),name="index"),
    path("deail/<int:post_id>/<slug:post_slug>/",views.DetailPostView.as_view(),name="post-detail")
    
]