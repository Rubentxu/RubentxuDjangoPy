from django.conf.urls.defaults import *

urlpatterns = patterns('blog.views',
    (r'^$', 'list_Posts'),
    (r'^sign$', 'create_Post')
)