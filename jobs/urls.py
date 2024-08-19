from django.urls import path
from . import views

urlpatterns = [
    path('get_filters/', views.get_filters, name='get_filters'),
    path('add_filter/', views.add_filter, name='add_filter'),
    path('remove_filter/', views.remove_filter, name='remove_filter'),
    path('clear_all_filters/', views.clear_filters, name='clear_all_filters'),
    path('show_countries/', views.show_all_countries, name='show_all_countries'),
    path('update_countries/', views.update_country_list, name='update_countries'),
    path('show_locations/<str:locations>', views.show_all_listing_locations, name='show_locations'), 
    path('render_filters_mobile/', views.render_filters_mobile, name='render_filters_mobile'),
    path('<slug:company>/<slug:opening>', views.get_individual_listing, name='individual_opening'),
    path('fetch_page/', views.fetch_page, name='fetch_page'),
    path('', views.load_main_page, name='job_listings'),
]