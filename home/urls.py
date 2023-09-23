from django.urls import path
from . import views


app_name = "home"
urlpatterns = [
    path("index/",views.IndexView.as_view(),name="index"),
    path("deail/<int:post_id>/<slug:post_slug>/",views.PostDetailView.as_view(),name="post-detail"),
    path("delete/<int:post_id>/",views.PostDeleteView.as_view(),name="post-delete"),
    path("update/<int:post_id>/",views.PostUpdateView.as_view(),name="post-update"),
    path("create/",views.PostCreateView.as_view(),name="post-create"),



    
]