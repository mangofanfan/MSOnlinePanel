from django import template

register = template.Library()

@register.simple_tag()
def site_url(url=""):
    return "http://localhost:8000/" + url