from django.shortcuts import render
from ..models import Job
from django.views.decorators.http import require_http_methods
from django.db.models import Q
from django.http import HttpResponse
from django.template import loader
from .util import categories, eu_countries, get_page_obj
from django.http import HttpRequest
import copy

DEFAULT_FILTERS = {'location': [], 'role': [], 'company': [], 'search': "", 'remote': False}
FILTER_KEYS = ["remote", "location", "company", "role", "search"]

def get_session_filters(request: HttpRequest) -> dict:
    return request.session.get('filters', copy.deepcopy(DEFAULT_FILTERS))

@require_http_methods(["GET"])
def get_filters(request: HttpRequest) -> HttpResponse:
    return render(request, 'jobs/partials/current_filters_partial.html', {"current_filters": get_session_filters(request)})

@require_http_methods(["GET"])
def update_company_list(request: HttpRequest) -> HttpResponse:
    filters = get_session_filters(request)
    companies = Job.objects.values('company').distinct().order_by('company')
    return render(request, 'jobs/partials/company_filter_partial.html', {"filtered_companies": filters['company'],
                  "companies": companies})

@require_http_methods(["GET"])
def update_role_list(request: HttpRequest) -> HttpResponse:
    filters = get_session_filters(request)
    return render(request, 'jobs/partials/category_filter_partial.html', {"categories": categories,
                  "current_filters": filters})

def render_job_list(request: HttpRequest, filters: dict) -> HttpResponse:
    """
    Utility function to render the job list based on the filters provided. 
    """
    query_set = process_filters(filters)
    jobs = Job.objects.filter(query_set).order_by('-created_at')
    page_obj = get_page_obj(jobs)
    
    request.session['filters'] = filters
    template = loader.get_template('jobs/job_list.html')
    response = HttpResponse(template.render({"page_obj": page_obj, "current_filters": filters}, request))
    response.headers["HX-Trigger"] = "filterChanged"
    return response

@require_http_methods(["POST"])
def add_filter(request: HttpRequest) -> HttpResponse:
    filters = get_session_filters(request)
    for key in FILTER_KEYS:
        value = request.POST.get(key)
        if value and key in filters and (key == 'remote' or value not in filters[key]) :
            if key == 'search':
                filters[key] = value
            elif key == 'remote' and value == 'on':
                filters[key] = True
            elif key == 'remote' and value == 'off':
                return remove_filter(request)
            else:
                filters[key].append(value)
        elif key == 'search' and not value:
            filters[key] = ""

    return render_job_list(request, filters)

@require_http_methods(["GET"])
def update_country_list(request: HttpRequest) -> HttpResponse:
    filters = get_session_filters(request)
    show_all = request.session.get('show_all_countries', False)
    if show_all:
        rendered_countries = eu_countries
    else:
        rendered_countries = eu_countries[:12]

    return render(request, 'jobs/partials/country_filter_partial.html', {"filtered_locations": filters['location'],
                  "eu_countries": rendered_countries, "show_all_countries": show_all})


def process_filters(filters) -> Q:
    """
    Processes the filters dict and return a Q object that can be used to filter the jobs from the db.
    """
    queries = {
        'location': Q(),
        'role': Q(),
        'company': Q(),
    }
    query_set = Q()
    for key, values in filters.items():
        if key in ['location', "company"] and values:
            queries[key] = add_query_filters(queries[key], key, values)
        elif key=='role' and values:
            queries[key] = process_role_filters(values)
        elif key == 'remote' and values:
            queries['remote'] = Q(remote=True)
        elif key == 'search' and values:
            queries['title'] = Q(title__icontains=values)

    for query in queries.values():
        query_set &= query
    return query_set

def add_query_filters(query_set, key, filters) -> Q:
    """
    Logical OR operation on filters for the same key. For example, if the filters are ['Germany', 'France'],
    the results should include jobs from Germany or France.
    """
    for filter in filters:
        query_set |= Q(**{f"{key}__icontains": filter})
    return query_set

def process_role_filters(roles):
    role_mappings = {
        'Software Development': ['Software', 'Software Developer', 'Software Engineering', 'Frontend Developer', 
                                 'QA Engineer', 'Engineering', 'Backend Developer', 'Fullstack Developer'],
        'Data & AI': ['Data Engineer', 'Data Science', 'Data Scientist/ML Engineer', "Data & AI",
                      ' Data Science & Analytics', 'ML Engineer', 'Head of Data Office'],
        'IT & Support': ['IT Services', 'Support Engineer', 'Developer Advocate', 'Information Systems - Information Technology',
                          'Product Manager'],
        'Cybersecurity': ['Cybersecurity', 'Security specialist', ' Security & Infrastructure'],
        'Hardware': ['Hardware', 'System'],
    }
    query_set = Q()
    for role in roles:
        if role in role_mappings:
            query_set |= Q(role__in=role_mappings.get(role))
    return query_set

@require_http_methods(["POST"])
def remove_filter(request: HttpRequest) -> HttpResponse:
    filters =  get_session_filters(request)
    if not filters:
        return HttpResponse(status=400)
    
    for key in FILTER_KEYS:
        value = request.POST.get(key)
        if value and key in filters and value in filters[key]:
            if key =="remote":
                filters.pop('remote')
            else:
                filters[key].remove(value)
    return render_job_list(request, filters)

@require_http_methods(["GET"])
def render_filters_mobile(request: HttpRequest) -> HttpResponse:
    filters = get_session_filters(request)
    companies = Job.objects.values('company').distinct().order_by('company')
    show = request.GET.get('show')
    request.session['show_all_countries'] = False

    if show == "True":
        return render(request, 'jobs/filters.html', {"current_filters": filters, "filtered_locations": filters['location'],
                                "eu_countries": eu_countries[:12], "companies": companies, "mobile_display": True, 
                                "categories": categories, "filtered_companies": filters['company'], "show_all_countries": False})
    else:
        return render(request, 'jobs/partials/mobile_filter_button_partial.html', {})

@require_http_methods(["POST"])
def clear_filters(request: HttpRequest) -> HttpResponse:
    return render_job_list(request, DEFAULT_FILTERS)