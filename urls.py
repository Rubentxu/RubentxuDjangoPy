from django.conf.urls.defaults import patterns, include, url
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import admin


handler500 = 'djangotoolbox.errorviews.server_error'

urlpatterns = patterns('',
    (r'^$', 'django.views.generic.simple.redirect_to', {'url': '/blog/', }),
    (r'^blog/', include('blog.urls')),

    (r'^accounts/create_user/$', 'blog.views.create_new_user'),
    (r'^accounts/login/$', 'django.contrib.auth.views.login',
        {'authentication_form': AuthenticationForm,
        'template_name': 'blog/login.html',}),
    (r'^accounts/logout/$', 'django.contrib.auth.views.logout',
        {'next_page': '/blog/',}),
    (r'^admin/doc/', include('django.contrib.admindocs.urls')),
    (r'^admin/', include(admin.site.urls)),
    
)
