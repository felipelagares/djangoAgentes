from django.db import models


class File(models.Model):
    id = models.AutoField(primary_key=True)
    file = models.FileField()
    objects = models.Manager()
    name = models.CharField(max_length=100)
