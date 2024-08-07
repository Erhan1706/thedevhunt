from django.shortcuts import render
from .models import Job
import ast

def job_listings(request):
    data = Job.objects.all()
    context = {"job_list": data}
    return render(request, 'jobs/jobs.html', context)

def opening(request, company, opening):
    job = Job.objects.get(company__iexact=company, slug__iexact=opening)
    return render(request, 'jobs/opening.html', {"job": job})

def show_all_locations(request, locations):
    locations  = ast.literal_eval(locations)
    context = {"locations": locations[3:]}
    return render(request, 'jobs/locations_partial.html', context)