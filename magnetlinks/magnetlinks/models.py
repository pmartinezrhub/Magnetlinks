# magnetlinks/models.py

from django.db import models
from django.contrib.auth.models import User

class Category(models.Model):
    category_name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.category_name


class MagnetLink(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=65)
    magnetlink = models.CharField(max_length=200, blank=True, null=True)
    filename = models.CharField(max_length=200, blank=True, null=True)
    description = models.CharField(max_length=2000, blank=True, null=True)
    imagelink = models.CharField(max_length=200, blank=True, null=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='magnet_links', default=1)
    seeders = models.IntegerField(default=0)
    leechers = models.IntegerField(default=0)
    date = models.DateField(auto_now_add=True)
    filesize = models.BigIntegerField(null=True)

    def __str__(self):
        return self.title

    def human_readable_size(self):
        value = self.filesize
        if not value:
            return
        if value < 1024:
            return f"{value} B"
        elif value < 1024**2:
            return f"{value / 1024:.1f} KB"
        elif value < 1024**3:
            return f"{value / 1024**2:.1f} MB"
        else:
            return f"{value / 1024**3:.1f} GB"
