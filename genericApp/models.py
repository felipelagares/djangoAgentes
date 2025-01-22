from django.db import models


class File(models.Model):
    id = models.AutoField(primary_key=True)
    file = models.FileField()
    objects = models.Manager()
    name = models.CharField(max_length=100)


class Film(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50)
    description = models.TextField()
    rating = models.FloatField()
    genres = models.TextField()
