from django import template

from Users.models import SiteUser

register = template.Library()

@register.simple_tag()
def get_avatar_src(user_id):
    return "/upload/file/" + SiteUser.objects.get(id=user_id).avatar + "/"