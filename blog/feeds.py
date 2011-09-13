from django.core.exceptions import ObjectDoesNotExist
from django.utils.feedgenerator import Atom1Feed
from django.contrib.syndication.feeds import Feed
from blog.models import Categoria, Post



class LatestEntriesFeed(Feed):
    author_name = "Ruben Dario"
    copyright = "AGPL" 
    description = "Ultimos Posts publicados" 
    feed_type = Atom1Feed
    item_copyright = "AGPL" 
    item_author_name = "Ruben Dario"
    item_author_link = "http://" 
    link = "/feeds/posts/"
    title = "Ultimos Posts" 
    
    def items(self):
        return Post.activo.all()[:15]
    
    def item_pubdate(self, item):
        return item.creado
    
    def item_guid(self, item):
        return "tag:%s:%s" % (item.creado.strftime('%Y-%m-%d'), item.get_absolute_url())
    
    



class CategoryFeed(LatestEntriesFeed):
    def get_object(self, bits):
        if len(bits) != 1:
            raise ObjectDoesNotExist
        return Categoria.objects.get(slug__exact=bits[0])
    
    def title(self, obj):
        return "Ultimos Posts en Categoria '%s'" % (obj.nombre)
    
    def description(self, obj):
        return "Ultimos Posts en Categoria '%s'" % (obj.nombre)
    
    def link(self, obj):
        return obj.get_absolute_url()
    
    def items(self, obj):
        return obj.live_post_set()[:15]
    