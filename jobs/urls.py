from django.urls import path
from . import views

urlpatterns = [
    path('', views.job_listings, name='job_listings'),
    path('<slug:company>/<slug:opening>', views.opening, name='individual-opening'),
]