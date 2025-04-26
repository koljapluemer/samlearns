from django.db import models

# Create your models here.
class Song(models.Model):
    title = models.CharField(max_length=200)
    artist = models.CharField(max_length=200)

class TabSheet(models.Model):
    song = models.ForeignKey(Song, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

class Beat(models.Model):
    tab_sheet = models.ForeignKey(TabSheet, on_delete=models.CASCADE)
    g = models.CharField(max_length=1)
    c = models.CharField(max_length=1)
    e = models.CharField(max_length=1)
    a = models.CharField(max_length=1)
