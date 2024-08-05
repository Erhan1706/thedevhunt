from rest_framework.response import Response
from rest_framework.decorators import api_view
from .serializers import JobSerializer
from .scrapers.scraper_factory import ScraperFactory

@api_view(['GET'])
def getJobs(request):
  scraper_factory = ScraperFactory()
  scraper = scraper_factory.get_scraper("jetbrains")
  listings = scraper.get_vacancies()

  serializer = JobSerializer(listings, many=True)
  return Response(serializer.data)
