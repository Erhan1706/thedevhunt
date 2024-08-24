from django.contrib import admin
from .models import Job
from django.utils.translation import gettext_lazy as _

class CountryListFilter(admin.SimpleListFilter):
  title= _('country')
  parameter_name = 'country'

  def lookups(self, request, model_admin):
    return [
      ('NL', 'Netherlands'),
      ('UK', 'United Kingdom'),
      ('GR', 'Germany'),
      ('FR', 'France'),
      ('CZ', 'Czech Republic'),
      ('PT', 'Portugal'),
    ]
  
  def queryset(self, request, queryset):
    if self.value() == 'NL':
      return queryset.filter(location__icontains='Netherlands')
    elif self.value() == 'UK':
      return queryset.filter(location__icontains='United Kingdom')
    elif self.value() == 'GR':
      return queryset.filter(location__icontains='Germany')
    elif self.value() == 'FR':
      return queryset.filter(location__icontains='France')
    elif self.value() == 'CZ':
      return queryset.filter(location__icontains='Czech Republic')
    elif self.value() == 'PT':
      return queryset.filter(location__icontains='Portugal')
    # can add more as needed

@admin.register(Job)
class JobAdmin(admin.ModelAdmin):
  date_hierarchy = 'created_at'
  list_filter = ['company', 'employment_type', 'remote', CountryListFilter, 'role']