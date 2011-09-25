from django.contrib import admin
from blog.models import Post , Categoria

def tags(instance):
    return ', '.join(instance.tags)

class PostAdmin(admin.ModelAdmin):
    list_display = ['titulo','categoria', tags]

admin.site.register(Post, PostAdmin)
admin.site.register(Categoria)
