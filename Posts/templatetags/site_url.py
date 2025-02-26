from django import template

register = template.Library()

@register.simple_tag()
def site_url(*args):
    return "http://localhost:8000/" + "".join(str(i) for i in args)