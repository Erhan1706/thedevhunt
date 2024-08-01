from django.urls import path
from . import views

urlpatterns = [
  path('', views.getJobs, name='getJobsApi'),
]