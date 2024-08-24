from django.shortcuts import render
from .models import Job
import ast
from django.shortcuts import get_object_or_404
from django.db.models import Q
from django.views.decorators.http import require_http_methods
from django.http import HttpResponse
from django.template import loader
from django.core.paginator import Paginator

eu_countries = ["Netherlands", "United Kingdom", "Germany", "France", "Austria", "Ireland", "Czech Republic", 
                    "Denmark", "Belgium", "Croatia", "Portugal", "Spain", "Romania", "Poland", "Norway", "Sweden",
                    "Cyprus", "Estonia", "Finland", "Greece", "Hungary", "Italy", "Bulgaria", "Switzerland", "Turkey",
                    "Iceland", "Latvia", "Lithuania", "Luxembourg", "Malta", "Russia", "Serbia", "Slovakia", 
                    "Ukraine", "Slovenia", "Belarus", "Bosnia and Herzegovina", "Moldova", "Montenegro",
                    "San Marino", "Vatican City", "Liechtenstein", "Albania","Kosovo", "Monaco", "North Macedonia", "Andorra"]


@require_http_methods(["GET"])
def load_main_page(request):
    filters = request.session.get('filters',{'locations': [], 'roles': [], 'technologies': [], 'companies':[]})
    query_set = process_filters(filters)
    jobs = Job.objects.filter(query_set)

    #t = Job.objects.values('role').distinct()
    companies = Job.objects.values('company').distinct().order_by('company')
    page_obj = get_page_obj(jobs)

    return render(request, 'jobs/content.html', {"eu_countries": eu_countries[:12], "page_obj": page_obj, "companies": companies,
                "show_all_countries": False, "current_filters": filters, "filtered_locations": filters['locations'],
                "filtered_companies": filters['companies']})

@require_http_methods(["GET"])
def fetch_page(request):
    filters = request.session.get('filters',{'locations': [], 'roles': [], 'technologies': [], 'companies': []})
    query_set = process_filters(filters)
    jobs = Job.objects.filter(query_set)

    page_num = request.GET.get("page")
    page_obj = get_page_obj(jobs, page_num)
    return render(request, 'jobs/job_list.html', {"page_obj": page_obj})

def get_page_obj(jobs, page_num=1):
    paginator = Paginator(jobs, 15)
    return paginator.get_page(page_num)

@require_http_methods(["GET"])
def get_individual_listing(request, company, opening):
    if company == "booking_com":
        company = "booking.com"
    t = Job.objects.filter(company__iexact=company, slug__iexact=opening)    
    job = get_object_or_404(Job, company__iexact=company, slug__iexact=opening)
    return render(request, 'jobs/listing.html', {"job": job})

@require_http_methods(["GET"])
def show_all_listing_locations(request, locations):
    locations  = ast.literal_eval(locations)
    context = {"locations": locations[3:]}
    return render(request, 'jobs/partials/listing_locations_partial.html', context)

@require_http_methods(["GET"])
def show_all_countries(request):
    filters = request.session.get('filters', {'locations': [], 'roles': [], 'technologies': [], 'companies': []})
    if request.GET.get('show_all') == 'True':
        request.session['show_all_countries'] = True
        return render(request, 'jobs/partials/country_filter_partial.html', {"filtered_locations": filters['locations'],
                      "eu_countries": eu_countries[12:], "show_all_countries": True})
    else:
        request.session['show_all_countries'] = False
        return render(request, 'jobs/partials/country_filter_partial.html', {"filtered_locations": filters['locations'],
                      "eu_countries": eu_countries[:12], "show_all_countries": False})

@require_http_methods(["GET"])
def update_country_list(request):
    filters = request.session.get('filters', {'locations': [], 'roles': [], 'technologies': [], 'companies': []})
    show_all = request.session.get('show_all_countries', False)
    if show_all:
        rendered_countries = eu_countries
    else:
        rendered_countries = eu_countries[:12]

    return render(request, 'jobs/partials/country_filter_partial.html', {"filtered_locations": filters['locations'],
                  "eu_countries": rendered_countries, "show_all_countries": show_all})

@require_http_methods(["GET"])
def update_company_list(request):
    filters = request.session.get('filters', {'locations': [], 'roles': [], 'technologies': [], 'companies': []})
    companies = Job.objects.values('company').distinct().order_by('company')
    return render(request, 'jobs/partials/company_filter_partial.html', {"filtered_companies": filters['companies'],
                  "companies": companies})

@require_http_methods(["POST"])
def add_filter(request):
    filters = request.session.get('filters', {'locations': [], 'roles': [], 'technologies': [], 'companies': []})
    remote = request.POST.get('remote')
    location = request.POST.get('country')
    company = request.POST.get('company')

    if remote:
        if remote == 'on':
            filters['remote'] = True
            #query_set |= Q(remote=True)
        if remote == 'off':
            return remove_filter(request)
    elif location and not location in filters['locations']:
        #query_set |= Q(location__icontains=location)
        filters['locations'].append(location)
    elif company and not company in filters['companies'] :
        #query_set |= Q(company__icontains=company)
        filters['companies'].append(company)

    query_set = process_filters(filters)
    jobs = Job.objects.filter(query_set)
    page_obj = get_page_obj(jobs)

    request.session['filters'] = filters
    template = loader.get_template('jobs/job_list.html')
    response = HttpResponse(template.render({"page_obj": page_obj, "current_filters": filters}, request))
    response.headers["HX-Trigger"] = "filterChanged"
    return response 

def process_filters(filters):
    queries = {
        'locations': Q(),
        'roles': Q(),
        'technologies': Q(),
        'companies': Q(),
    }
    query_set = Q()
    for key, values in filters.items():
        if key=='locations' and values:
            queries[key] = Q(**{"location__icontains":value for value in values})
        elif key=='roles' and values:
            queries[key] = Q(**{"role__icontains": value for value in values})
        elif key=='technologies' and values:
            queries[key] = Q(**{"technologies__icontains": value for value in values})
        elif key=='companies' and values:
            queries[key] = Q(**{"company__icontains": value for value in values})
        elif key == 'remote' and values:
            queries['remote'] = Q(remote=True)

    for query in queries.values():
        query_set &= query
    return query_set

@require_http_methods(["POST"])
def remove_filter(request):
    filters = request.session.get('filters')
    if not filters:
        return HttpResponse(status=400)
    
    location = request.POST.get('country')
    remote = request.POST.get('remote')
    company = request.POST.get('company')

    if remote and remote == 'off':
        filters.pop('remote')
    elif location:
        filters['locations'].remove(location)
    elif company:
        filters['companies'].remove(company)

    query_set = process_filters(filters)
    jobs = Job.objects.filter(query_set)
    request.session['filters'] = filters
    page_obj = get_page_obj(jobs)

    template = loader.get_template('jobs/job_list.html')
    response = HttpResponse(template.render({"page_obj": page_obj, "current_filters": filters}, request))
    response.headers["HX-Trigger"] = "filterChanged"
    return response 


@require_http_methods(["GET"])
def get_filters(request):
    return render(request, 'jobs/partials/current_filters_partial.html', {"current_filters": request.session.get('filters')})

@require_http_methods(["GET"])
def render_filters_mobile(request):
    filters = request.session.get('filters',{'locations': [], 'roles': [], 'technologies': [], 'companies':[]})
    companies = Job.objects.values('company').distinct().order_by('company')
    show = request.GET.get('show')
    if show == "True":
        return render(request, 'jobs/filters.html', {"current_filters": filters, "filtered_locations": filters['locations'],
                                "eu_countries": eu_countries[:12], "companies": companies, "mobile_display": True})
    else:
        return render(request, 'jobs/partials/mobile_filter_button_partial.html', {})

@require_http_methods(["POST"])
def clear_filters(request):
    request.session['filters'] = {'locations': [], 'roles': [], 'technologies': [], 'companies': []}
    jobs = Job.objects.all()
    page_obj = get_page_obj(jobs)

    template = loader.get_template('jobs/job_list.html')
    response = HttpResponse(template.render({"page_obj": page_obj, "current_filters": request.session.get('filters')}, request))
    response.headers["HX-Trigger"] = "filterChanged"
    return response