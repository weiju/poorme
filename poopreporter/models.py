from django.db import models

class Food(models.Model):
  name = models.CharField(max_length=200)

class Symptom(models.Model):
  name = models.CharField(max_length=200)

class Neighborhood(models.Model):
  name = models.CharField(max_length=200)
