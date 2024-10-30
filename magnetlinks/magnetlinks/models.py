# magnetlinks/models.py

from django.db import models

class MagnetLink(models.Model):
    title = models.CharField(max_length=65)
    magnetlink = models.CharField(max_length=200, blank=True, null=True)
    filename = models.CharField(max_length=200, blank=True, null=True)
    description = models.CharField(max_length=400, blank=True, null=True)
    imagelink = models.CharField(max_length=200, blank=True, null=True)
    seeders = models.IntegerField(default=0)
    leechers = models.IntegerField(default=0)
    date = models.DateField(auto_now_add=True)
    
    def __str__(self):
        return self.title
