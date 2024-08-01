from rest_framework.response import Response
from rest_framework.decorators import api_view
from .scraper_intellij import get_vacancies

@api_view(['GET'])
def getJobs(request):
  return Response(get_vacancies())
