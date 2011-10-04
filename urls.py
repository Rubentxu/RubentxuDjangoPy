from django.conf.urls.defaults import patterns, include, url
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import admin
from blog.feeds import LatestEntriesFeed,CategoryFeed
from blog.Sitemap import all_sitemaps as sitemaps
from django.views.generic import TemplateView

admin.autodiscover()
handler500 = 'djangotoolbox.errorviews.server_error'

feeds = {
    'ultimos': LatestEntriesFeed,
    'categorias': CategoryFeed,
}

urlpatterns = patterns('',
    (r'^$', 'django.views.generic.simple.redirect_to', {'url': '/blog/', }),
    (r'^blog/', include('blog.urls')),
    (r'^accounts/create_user/$', 'blog.views.create_new_user'),
    (r'^accounts/login/$', 'django.contrib.auth.views.login',
        {'authentication_form': AuthenticationForm,
        'template_name': 'blog/login.html',
        }),
    (r'^accounts/logout/$', 'django.contrib.auth.views.logout',
        {'next_page': '/blog/',}),    
    (r'^admin/', include(admin.site.urls)),
    (r'^markdown/preview/$', 'blog.views.mark'),
    (r'^comments/', include('django.contrib.comments.urls')),
    (r'^feeds/(?P<url>.*)/$', 'django.contrib.syndication.views.feed', {'feed_dict': feeds}),   
    
    (r'^sitemap.xml$', 'django.contrib.sitemaps.views.index', {'sitemaps': sitemaps}),
    (r'^sitemap-(?P<section>.+)\.xml$', 'django.contrib.sitemaps.views.sitemap', {'sitemaps': sitemaps}),
    (r'^favicon\.ico$', 'django.views.generic.simple.redirect_to', {'url': '/media/images/favicon.ico'}),
    (r'^acercade/', TemplateView.as_view(template_name="acerca.html")),   
    (r'^buscar/', TemplateView.as_view(template_name="buscar.html")),
    
)
