from django.db import models
from django.contrib.auth.models import User

class Symptom(models.Model):
    name = models.CharField(max_length=200)
    
class Stuff(models.Model):
    name = models.CharField(max_length=200)

class Comment(models.Model):
    author = models.CharField(max_length=200)
    text = models.CharField(max_length=1000)

class Status(models.Model):
    name = models.CharField(max_length=100)
    status = models.ForeignKey(Comment)
    zipcode = models.CharField(max_length=20)
    symptoms = models.ManyToManyField(Symptom)
    replies = models.ManyToManyField(Comment, related_name='+')
    wishlist = models.ManyToManyField(Stuff)


class LoggedInComment(models.Model):
    user = models.ForeignKey(User, related_name='+')
    time = models.DateTimeField(auto_now=True, auto_now_add=True)
    text = models.CharField(max_length=1000)
    
class Incident(models.Model):
    user = models.ForeignKey(User, related_name='+')
    created = models.DateTimeField(auto_now=True, auto_now_add=True)
    wishlist = models.ManyToManyField(Stuff)
    zipcode = models.CharField(max_length=20)
    comments = models.ForeignKey(LoggedInComment)
    
class Update(models.Model):
    incident = models.ForeignKey(Incident)
    time = models.DateTimeField(auto_now=True, auto_now_add=True)
    text_status = models.CharField(max_length=1000)
    symptoms = models.ManyToManyField(Symptom)
    