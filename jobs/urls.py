from django.urls import path
from .views import listings, filters, companies_list, main_page

urlpatterns = [
    path('get_filters/', filters.get_filters, name='get_filters'),
    path('add_filter/', filters.add_filter, name='add_filter'),
    path('remove_filter/', filters.remove_filter, name='remove_filter'),
    path('clear_all_filters/', filters.clear_filters, name='clear_all_filters'),
    path('show_countries/', listings.show_all_countries, name='show_all_countries'),
    path('update_countries/', filters.update_country_list, name='update_countries'),
    path('update_companies/', filters.update_company_list, name='update_companies'),
    path('update_roles/', filters.update_role_list, name='update_roles'),
    path('show_locations/<str:locations>', listings.show_all_listing_locations, name='show_locations'), 
    path('render_filters_mobile/', filters.render_filters_mobile, name='render_filters_mobile'),
    path('<slug:company>/<slug:opening>', listings.get_individual_listing, name='individual_opening'),
    path('fetch_page/', listings.fetch_page, name='fetch_page'),
    path('companies/', companies_list.render_companies_list_page, name='companies_list'),
    path('listings/', listings.load_main_page, name='job_listings'),
    path('', main_page.load_landing_page, name='main_page'),
]