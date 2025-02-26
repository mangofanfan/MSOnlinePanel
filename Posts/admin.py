from django.contrib import admin

from Posts.models import Post, Notice

admin.site.register(Post)
admin.site.register(Notice)
