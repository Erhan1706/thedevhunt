from django.shortcuts import render
from django.http import HttpRequest, HttpResponse
from django.views.decorators.http import require_http_methods

@require_http_methods(["GET"])
def load_landing_page(request: HttpRequest) -> HttpResponse:
    return render(request, 'jobs/main_page.html')