from django.db import models

class Job(models.Model):
  title = models.CharField(max_length=400)
  slug = models.SlugField(max_length=200)
  description = models.TextField()
  role = models.CharField(max_length=400)
  technologies = models.JSONField(null=True)
  location = models.JSONField()
  company = models.CharField(max_length=200)
  remote = models.BooleanField()
  last_modified = models.DateTimeField(auto_now=True, null=True)
  link_to_apply = models.URLField()
  created_at = models.DateTimeField(null=True)
  employment_type = models.CharField(
      max_length=100,
      choices=[
          ('FULL_TIME', 'Full-time'),
          ('INTERNSHIP', 'Internship'),
          ('PART_TIME', 'Part-time'),  # Optional: if you want to include this type
      ],
      default='FULL_TIME')