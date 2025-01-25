from django.db import models


class File(models.Model):
    id = models.AutoField(primary_key=True)
    file = models.FileField()
    objects = models.Manager()
    name = models.CharField(max_length=100)


class Film(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=50)
    description = models.TextField(null=True, blank=True)
    rating = models.FloatField(null=True, blank=True)
    genres = models.TextField(null=True, blank=True)
    clean_desc = models.TextField(null=True, blank=True)
    objects = models.Manager()
