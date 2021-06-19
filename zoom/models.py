from django.db import models

# Create your models here.
class StoreData(models.Model):
    event = models.CharField(max_length=100)
    uiud = models.CharField(max_length=100)
    starttime = models.CharField(max_length=100)
    topic = models.CharField(max_length=500)
    email = models.CharField(max_length=100)
    user_id = models.CharField(max_length=100)
    jointime = models.CharField(max_length=100)
    username = models.CharField(max_length=100)
    startdate = models.CharField(max_length=100)
    authtoken = models.CharField(max_length=100)

    def __str__(self):
        return self.username + ' : ' + self.event + ' : ' + self.topic +' : '+ self.jointime

class AuthIds(models.Model):
    username = models.CharField(max_length=100)
    authtoken = models.CharField(max_length=100)

    def __str__(self):
        return self.username + ":" + self.authtoken

class Files(models.Model):
    username = models.CharField(max_length=100)
    name = models.CharField(max_length=100)
    content = models.TextField()

    def __str__(self):
        return self.username + ":" + self.name

class CurrentMeetinglog(models.Model):
    authtoken = models.CharField(max_length=100)
    starttime = models.CharField(max_length=100)
    startdate = models.CharField(max_length=100)
    topic = models.CharField(max_length=500)
    def __str__(self):
        return self.authtoken + ":" + self.starttime

class ReportLog(models.Model):
    username=models.CharField(max_length=100)
    starttime = models.CharField(max_length=100)
    startdate = models.CharField(max_length=100)
    topic = models.CharField(max_length=500)
    report = models.TextField()

    def __str__(self):
        return self.username + ":" + self.starttime + ":" + self.startdate + ":" +self.topic

class Metrics(models.Model):
    username = models.CharField(max_length=100)
    late = models.CharField(max_length=100)
    leftearly = models.CharField(max_length=100)
    minduration = models.CharField(max_length=100)

    def __str__(self):
        return self.username
