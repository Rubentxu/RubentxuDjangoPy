from django.contrib import admin
from blog.models import Post, Comentario, Tag, Categoria

admin.site.register(Post)
admin.site.register(Comentario)
admin.site.register(Tag)
admin.site.register(Categoria)