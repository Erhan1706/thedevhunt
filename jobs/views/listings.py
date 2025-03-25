from django.shortcuts import render
from ..models import Job
import ast
from django.shortcuts import get_object_or_404
from django.views.decorators.http import require_http_methods
from .filters import process_filters, get_session_filters
from .util import eu_countries, categories, get_page_obj
from django.http import HttpRequest, HttpResponse

"""
Loads the main page with all the job listings. Content.html is the base layout + filter layout + some extra information.
Within content.html, job_list.html is loaded with the job listings.
"""
@require_http_methods(["GET"])
def load_main_page(request: HttpRequest) -> HttpResponse:
    filters = get_session_filters(request)
    request.session['show_all_countries'] = False
    query_set = process_filters(filters)
    jobs = Job.objects.filter(query_set).order_by('-created_at')

    companies = Job.objects.values('company').distinct().order_by('company')
    page_obj = get_page_obj(jobs)

    return render(request, 'jobs/content.html', {"eu_countries": eu_countries[:12], "page_obj": page_obj, "companies": companies,
                "show_all_countries": False, "current_filters": filters, "filtered_locations": filters['location'],
                "filtered_companies": filters['company'],"categories": categories})

@require_http_methods(["GET"])
def fetch_page(request: HttpRequest) -> HttpResponse:
    """
    Fetches the individual listing page for a singular job. 
    """
    filters = get_session_filters(request)
    query_set = process_filters(filters)
    jobs = Job.objects.filter(query_set).order_by('-created_at')

    page_num = request.GET.get("page")
    page_obj = get_page_obj(jobs, page_num)
    return render(request, 'jobs/job_list.html', {"page_obj": page_obj})


@require_http_methods(["GET"])
def get_individual_listing(request: HttpRequest, company: str, opening: str) -> HttpResponse:
    if company == "booking_com":
        company = "booking.com"
        
    job = get_object_or_404(Job, company__iexact=company, slug__iexact=opening)
    return render(request, 'jobs/listing.html', {"job": job})

@require_http_methods(["GET"])
def show_all_listing_locations(request: HttpRequest, locations) -> HttpResponse:
    locations  = ast.literal_eval(locations)
    context = {"locations": locations[3:]}
    return render(request, 'jobs/partials/listing_locations_partial.html', context)

@require_http_methods(["GET"])
def show_all_countries(request: HttpRequest) -> HttpResponse:
    filters = get_session_filters(request)
    if request.GET.get('show_all') == 'True':
        request.session['show_all_countries'] = True
        return render(request, 'jobs/partials/country_filter_partial.html', {"filtered_locations": filters['location'],
                      "eu_countries": eu_countries[12:], "show_all_countries": True})
    else:
        request.session['show_all_countries'] = False
        return render(request, 'jobs/partials/country_filter_partial.html', {"filtered_locations": filters['location'],
                      "eu_countries": eu_countries[:12], "show_all_countries": False})
