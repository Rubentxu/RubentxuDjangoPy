from django.contrib import admin
from blog.models import Post,  Tag, Categoria

admin.site.register(Post)
admin.site.register(Tag)
admin.site.register(Categoria)