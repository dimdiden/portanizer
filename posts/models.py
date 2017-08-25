from django.urls import reverse
from django.db import models
from django.contrib.auth.models import User


class Post(models.Model):
    user = models.ForeignKey(User)
    title = models.CharField(max_length=50)
    body = models.TextField()
    tag = models.ManyToManyField('Tag', blank=True)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('posts:update', kwargs={'pk': str(self.id)})


class Tag(models.Model):
    user = models.ForeignKey(User)
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name
