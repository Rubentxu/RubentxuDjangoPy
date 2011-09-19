from django.contrib import admin
from blog.models import *

admin.site.register(Post)
admin.site.register(Tag)
admin.site.register(Categoria)
admin.site.register(Post_Tag)