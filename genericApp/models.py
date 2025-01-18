from django.db import models


class File(models.Model):
    id = models.AutoField(primary_key=True)
    file = models.FileField()
    objects = models.Manager()
    name = models.CharField(max_length=100)


class Person(models.Model):
    id = models.IntegerField(primary_key=True)
    Age = models.IntegerField()
    Gender = models.CharField(max_length=6)
    UndergraduateMajor = models.CharField()
    UndergraduateGPA = models.FloatField()
    YearsOfWorkExperience = models.IntegerField()
    CurrentJobTitle = models.CharField(max_length=100)
    AnnualSalary = models.IntegerField()
    HasManagementExperience = models.BooleanField()
    GreGmatScore = models.IntegerField()
    UndergradUniversityRanking = models.IntegerField()
    EntrepreneurialInterest = models.IntegerField()
    NetworkingImportance = models.FloatField()
    MbaFundingSource = models.CharField()
    DesiredPostMbaRole = models.CharField()
    ExpectedPostMbaSalary = models.IntegerField()
    LocationPreferencePostMba = models.CharField()
    ReasonForMba = models.CharField()
    OnlinePresentialMba = models.CharField()
    DecidedToMba = models.BooleanField()
