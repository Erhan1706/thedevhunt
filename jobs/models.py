from django.db import models

class Job(models.Model):
  title = models.CharField(max_length=200)
  slug = models.SlugField(max_length=200)
  description = models.TextField()
  role = models.CharField(max_length=200)
  technologies = models.JSONField()
  location = models.JSONField()
  company = models.CharField(max_length=200)
  remote = models.BooleanField()
  last_modified = models.DateTimeField(auto_now=True)