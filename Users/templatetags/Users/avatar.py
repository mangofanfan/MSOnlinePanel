from django import template

from Users.models import SiteUser

register = template.Library()

@register.simple_tag()
def get_avatar_src(user_id):
    if (md5:=SiteUser.objects.get(id=user_id).avatar) is not None:
        return "/upload/file/" + md5 + "/"
    else:
        return "/static/Users/liuyingQAQ.jpg"