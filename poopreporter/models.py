from django.db import models

class Food(models.Model):
  name = models.CharField(max_length=200)

class Symptom(models.Model):
  name = models.CharField(max_length=200)

class Neighborhood(models.Model):
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

class Zipcode(models.Model):
  zipcode = models.CharField(max_length=20)
  longitude = models.DecimalField(max_digits=9, decimal_places=6)
  latitude = models.DecimalField(max_digits=9, decimal_places=6)
