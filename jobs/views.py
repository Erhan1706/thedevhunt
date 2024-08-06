from django.shortcuts import render
from .models import Job
import ast

def job_listings(request):
    data = Job.objects.all()
    context = {"job_list": data}
    return render(request, 'jobs/jobs.html', context)

def opening(request, company, opening):
    return render(request, 'jobs/opening.html')

def show_all_locations(request, locations):
    arr  = ast.literal_eval(locations)
    context = {"locations": arr}
    return render(request, 'jobs/locations_partial.html', context)