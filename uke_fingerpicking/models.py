from django.db import models


class TabSheet(models.Model):
    title = models.CharField(max_length=200)
    artist = models.CharField(max_length=200)
    created_at = models.DateTimeField(auto_now_add=True)

class Beat(models.Model):
    index = models.IntegerField()
    tab_sheet = models.ForeignKey(TabSheet, on_delete=models.CASCADE)
    a = models.CharField(max_length=1)
    e = models.CharField(max_length=1)
    c = models.CharField(max_length=1)
    g = models.CharField(max_length=1)
