from django.conf.urls.defaults import *
from blog.models import *
from blog.views import *

urlpatterns = patterns('blog.views',    
    (r'^(?P<slug>[-\w]+)/$', categoria_detalle, {}, 'categoria_detalle'),    
    (r'^$', index_Posts, { 'pagina':1}),
    (r'^post/pagina/(?P<pagina>\d{0,3})$', index_Posts),
    (r'^post/listpost/$',lista_Posts),    
    (r'^post/verpost/(?P<slug>[-\w]+)/$',ver_Post),
    (r'^post/crearpost/$', crear_Post),
    (r'^post/modifpost/(?P<slug>[-\w]+)/$',modificar_Post),
    (r'^post/borrarpost/(?P<slug>[-\w]+)/$',borrar_Post),
    (r'^tag/(?P<tag>[\w]+)/pagina/(?P<pagina>\d{0,3})/$',lista_Post_Tag),
    (r'^cat/(?P<catg>[\w]+)/pagina/(?P<pagina>\d{0,3})/$',lista_Post_Categoria),
)