from django.conf.urls.defaults import *
from blog.models import *

urlpatterns = patterns('blog.views',    
    (r'^(?P<slug>[-\w]+)/$', 'categoria_detalle', {}, 'categoria_detalle'),    
    (r'^$', 'index_Posts'),
    (r'^post/listpost/$','lista_Posts'),    
    (r'^post/verpost/(?P<clave>\d+)/$','ver_Post'),
    (r'^post/crearpost/$','crear_Post'),
    (r'^post/modifpost/(?P<clave>\d+)/$','modificar_Post'),
    (r'^post/borrarpost/(?P<clave>\d+)/$','borrar_Post'),
)