from django.shortcuts import render
from django.views.decorators.http import require_http_methods
from ..models import Job
from django.http import HttpRequest, HttpResponse


@require_http_methods(["GET"])
def render_companies_list_page(request: HttpRequest) -> HttpResponse:
    companies = Job.objects.values('company').distinct().order_by('company')
    return render(request, 'jobs/companies_list.html', {"companies": companies})
