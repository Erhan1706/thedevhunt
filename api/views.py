from rest_framework.response import Response
from rest_framework.decorators import api_view
from .serializers import JobSerializer
from .scrapers.scraper_factory import ScraperFactory
from jobs.models import Job

@api_view(['GET'])
def getJobs(request):
  scraper_factory = ScraperFactory()
  scraper = scraper_factory.get_scraper("jetbrains")
  listings = scraper.get_vacancies()

  updated_jobs = []
  created_jobs = []

  for job in listings:
    existing_job = Job.objects.filter(slug=job['slug']).first()

    if existing_job:
      serializer = JobSerializer(existing_job, data=job, partial=True)
      if serializer.is_valid():
          serializer.save()
          updated_jobs.append(serializer.data)
    else:
      serializer = JobSerializer(data=job)
      if serializer.is_valid():
          serializer.save()
          created_jobs.append(serializer.data)

  return Response(serializer.data)
