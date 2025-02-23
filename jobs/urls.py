from django.urls import path
from .views import main, filters

urlpatterns = [
    path('get_filters/', filters.get_filters, name='get_filters'),
    path('add_filter/', filters.add_filter, name='add_filter'),
    path('remove_filter/', filters.remove_filter, name='remove_filter'),
    path('clear_all_filters/', filters.clear_filters, name='clear_all_filters'),
    path('show_countries/', main.show_all_countries, name='show_all_countries'),
    path('update_countries/', filters.update_country_list, name='update_countries'),
    path('update_companies/', filters.update_company_list, name='update_companies'),
    path('update_roles/', filters.update_role_list, name='update_roles'),
    path('show_locations/<str:locations>', main.show_all_listing_locations, name='show_locations'), 
    path('render_filters_mobile/', filters.render_filters_mobile, name='render_filters_mobile'),
    path('<slug:company>/<slug:opening>', main.get_individual_listing, name='individual_opening'),
    path('fetch_page/', main.fetch_page, name='fetch_page'),
    path('', main.load_main_page, name='job_listings'),
]