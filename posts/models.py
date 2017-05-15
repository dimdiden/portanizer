from django.db import models

"""
https://docs.djangoproject.com/en/1.11/topics/db/models/#fields
The default HTML widget to use when rendering a form field (e.g. <input type="text">, <select>).
"""


class Post(models.Model):
    title = models.CharField(max_length=50)
    body = models.TextField()

    def __str__(self):
        return self.title
