from django.shortcuts import render
from .models import Job
import ast
from django.shortcuts import get_object_or_404
from django.db.models import Q
from django.views.decorators.http import require_http_methods
from django.http import HttpResponse
from django.template import loader


eu_countries = ["Netherlands", "United Kingdom", "Germany", "France", "Austria", "Ireland", "Czech Republic", 
                    "Denmark", "Belgium", "Croatia", "Portugal", "Spain", "Romania", "Poland", "Norway", "Sweden",
                    "Cyprus", "Estonia", "Finland", "Greece", "Hungary", "Italy", "Bulgaria", "Switzerland", "Turkey",
                    "Iceland", "Latvia", "Lithuania", "Luxembourg", "Bulgaria", "Malta", "Russia", "Serbia", "Slovakia", 
                    "Ukraine", "Slovenia", "Bulgaria", "Belarus", "Bosnia and Herzegovina", "Moldova", "Montenegro",
                    "San Marino", "Vatican City", "Liechtenstein", "Albania","Kosovo", "Monaco", "North Macedonia", "Andorra"]

@require_http_methods(["GET"])
def load_main_page(request):
    filters = request.session.get('filters')
    query_set = process_filters(filters, Q())
    jobs = Job.objects.filter(query_set)

    return render(request, 'jobs/content.html', {"job_list": jobs, "eu_countries": eu_countries[:12], 
                                              "show_all_countries": False, "current_filters": filters})

@require_http_methods(["GET"])
def get_individual_listing(request, company, opening):
    job = get_object_or_404(Job, company__iexact=company, slug__iexact=opening)
    return render(request, 'jobs/listing.html', {"job": job})

@require_http_methods(["GET"])
def show_all_locations(request, locations):
    locations  = ast.literal_eval(locations)
    context = {"locations": locations[3:]}
    return render(request, 'jobs/partials/listing_locations_partial.html', context)

@require_http_methods(["GET"])
def show_all_countries(request):
    if request.GET.get('show_all') == 'true':
        return render(request, 'jobs/partials/country_filter_partial.html', {"eu_countries": eu_countries[12:], "show_all_countries": True})
    else:
        return render(request, 'jobs/partials/country_filter_partial.html', {"eu_countries": eu_countries[:12], "show_all_countries": False})

@require_http_methods(["POST"])
def add_filter(request):
    filters = request.session.get('filters', {'locations': [], 'roles': [], 'technologies': []})
    query_set = process_filters(filters, Q())

    remote = request.POST.get('remote')
    location = request.POST.get('country')

    if remote and remote == 'on':
        query_set &= Q(remote=True)
        filters['remote'] = True
    elif location:
        query_set &= Q(location__icontains=location)
        filters['locations'].append(location)
        eu_countries.remove(location)

    jobs = Job.objects.filter(query_set)

    request.session['filters'] = filters
    template = loader.get_template('jobs/job_list.html')
    response = HttpResponse(template.render({"job_list": jobs, "current_filters": filters}, request))
    response.headers["HX-Trigger"] = "filterChanged"
    return response 

def process_filters(filters, query_set):
    for key in filters.keys():
        if key == 'locations':
            for location in filters[key]:
                query_set &= Q(location__icontains=location)
        elif key == 'remote' and filters[key]:
            query_set &= Q(remote=True)
        elif key == 'roles':
            for role in filters[key]:
                query_set &= Q(role__icontains=role)
        elif key == 'technologies':
            for tech in filters[key]:
                query_set &= Q(technologies__icontains=tech)
                        
    return query_set

@require_http_methods(["POST"])
def remove_filter(request):
    filters = request.session.get('filters')
    if not filters:
        return HttpResponse(status=400)
    
    location = request.POST.get('country')
    if location:
        filters['locations'].remove(location)
        eu_countries.insert(0, location)

    query_set = process_filters(filters, Q())
    jobs = Job.objects.filter(query_set)
    request.session['filters'] = filters

    template = loader.get_template('jobs/job_list.html')
    response = HttpResponse(template.render({"job_list": jobs, "current_filters": filters}, request))
    response.headers["HX-Trigger"] = "filterChanged"
    return response 


@require_http_methods(["GET"])
def get_filters(request):
    return render(request, 'jobs/partials/current_filters_partial.html', {"current_filters": request.session.get('filters')})