from django import template
register = template.Library()

@register.inclusion_tag('jobs/partials/listing_locations_partial.html')
def show_locations(locations, startIndex=None, endIndex=None):
  if startIndex is None and endIndex is None:
      return {'locations': locations}
  elif endIndex is None:
     return {'locations': locations[startIndex:]}
  else:
    return {'locations': locations[startIndex:endIndex]}