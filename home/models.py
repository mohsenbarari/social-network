from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse



class Post(models.Model):
    title = models.CharField(max_length=50)
    body = models.TextField(max_length=700)
    slug = models.SlugField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(User,on_delete=models.CASCADE,related_name="posts")

    def get_absolute_url(self):
        return reverse("home:post-detail",args=(self.id,self.slug))
