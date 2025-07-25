from django.shortcuts import render
from django.http import HttpRequest, HttpResponse
from django.views.decorators.http import require_http_methods

from jobs.models import Job
from django.core.cache import cache


def round_to_hundred(n):
    return (n // 100) * 100

@require_http_methods(["GET"])
def load_landing_page(request: HttpRequest) -> HttpResponse:
    total_jobs = cache.get('total_jobs_count')
    if total_jobs is None:
        total_jobs = Job.objects.count()
        cache.set('total_jobs_count', total_jobs, 300)  # cache for 5 minutes

    total_jobs = round_to_hundred(total_jobs)
    return render(request, 'jobs/main_page.html', {"total_jobs": total_jobs})