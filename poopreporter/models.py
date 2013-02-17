from django.db import models
from django.contrib.auth.models import User
from django.utils import timesince

from datetime import *

class Symptom(models.Model):
    name = models.CharField(max_length=200)
    
class Stuff(models.Model):
    name = models.CharField(max_length=200)

class Episode(models.Model):
    user = models.ForeignKey(User, related_name='+')
    started = models.DateTimeField(auto_now=True, auto_now_add=True)
    ended = models.DateTimeField(blank=True, null=True)
    wishlist = models.ManyToManyField(Stuff)
    zipcode = models.CharField(max_length=20)
    
    def description(self):
        updates = Update.objects.select_related("episode").filter(episode=self)
        symptom_set = set()
        for update in updates:
            for symptom in update.symptoms.all():
                symptom_set.add(symptom.name)
        return ", ".join(symptom_set)
        
    def duration(self): 
        if self.ended == None:
            ts = self.started- self.started
            days = ts.days + 1
            return "%d days" % days
        else:
            print timesince(self.started, self.ended)
            days = ts.days + 1
            return "%d days" % days
            
    def status(self):
        user_comment = LoggedInComment.objects.select_related("episode").filter(episode=self).order_by("time")[0]
        return user_comment.text
        
    
class Update(models.Model):
    time = models.DateTimeField(auto_now=True, auto_now_add=True)
    symptoms = models.ManyToManyField(Symptom)
    episode = models.ForeignKey(Episode)
    
class LoggedInComment(models.Model):
    user = models.ForeignKey(User, related_name='+')
    time = models.DateTimeField(auto_now=True, auto_now_add=True)
    text = models.CharField(max_length=1000)
    episode = models.ForeignKey(Episode)
    



    
    
