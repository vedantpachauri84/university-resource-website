from django.db import models

# Create your models here.
from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver


class Profile(models.Model):
        user = models.OneToOneField(User, on_delete=models.CASCADE)
        image = models.ImageField(upload_to='profile_pics/', default='default.jpg')

        def __str__(self):
            return self.user.username
class Paper(models.Model):
    title = models.CharField(max_length=100)
    year = models.IntegerField()
    file=models.FileField(upload_to='Papers/')
    def __str__(self):
        return self.title
class Notes(models.Model):
    title = models.CharField(max_length=100)
    Subject = models.CharField(max_length=100)
    file=models.FileField(upload_to='Notes/')
    def __str__(self):
        return self.title
class Resources(models.Model):
    title = models.CharField(max_length=100)
    Subject = models.CharField(max_length=100)
    File = models.FileField(upload_to='Resources/')
    def __str__(self):
        return self.title
class Blog(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)
    image = models.ImageField(upload_to='blog/')
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
class Contact(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    message = models.TextField()