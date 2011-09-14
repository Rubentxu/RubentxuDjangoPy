### sitemaps.py
from django.contrib.sitemaps import GenericSitemap
from blog.models import Post, Categoria

all_sitemaps = {}
for categoria in Categoria.objects.all():

    info_dict = {
        'queryset': categoria.post_set.filter(estado=1),
    }

    sitemap = GenericSitemap(info_dict,priority=0.6)

    # dict key is provided as 'section' in sitemap index view
    all_sitemaps[categoria.nombre] = sitemap
