from rest_framework import serializers
from jobs.models import Job

class JobSerializer(serializers.ModelSerializer):
  class Meta:
    model = Job
    fields = ['id', 'title', 'slug', 'description', 'role', 'technologies', 'location', 'company', 'remote', 'link_to_apply']