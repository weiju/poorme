from django.db import models


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
