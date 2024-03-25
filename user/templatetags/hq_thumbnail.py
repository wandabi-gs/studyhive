from django import template 
from django.urls import resolve
  
register = template.Library() 
  
@register.filter(name="hq_thumbnail") 
def hq_thumbnail(input_string):
    try:
        return input_string.replace("default", "hqdefault")
    
    except:
        return input_string
    
@register.simple_tag(takes_context=True)
def current_route(context):

    try:
        request = context["request"]
        return resolve(request.path_info).url_name
    except:
        return None
    
@register.filter(name="route_name")
def route_name(route):
    try:
        routeName = str(route)
        routeName = routeName.replace("-", " ")
        routes = routeName.split(" ")
        cap_routes = []

        for i in range(len(routes)):
            cap_routes.append(routes[i].capitalize())

        routeName = " ".join(cap_routes)

        return routeName
    except:
        return None


