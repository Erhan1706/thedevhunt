from django.urls import path
from . import views

urlpatterns = [
    path('show_locations/<str:locations>', views.show_all_locations, name='show_locations'), 
    path('<slug:company>/<slug:opening>', views.opening, name='individual_opening'),
    path('', views.job_listings, name='job_listings'),
]