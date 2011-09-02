from django.core.cache import cache
from django.contrib.auth.forms import UserCreationForm
from django.views.generic.simple import direct_to_template
from django.http import HttpResponseRedirect
from django.views.generic.simple import direct_to_template
from blog.forms import CreatePostForm
from blog.models import Post

MEMCACHE_Post = 'Post'

def list_Posts(request):
    Posts = cache.get(MEMCACHE_Post)
    if Posts is None:
        Posts = Post.objects.all().order_by('-fecha')[:10]
        cache.add(MEMCACHE_Post, Posts)
    return direct_to_template(request, 'blog/index.html',
                              {'Posts': Posts,
                               'form': CreatePostForm()})

def create_Post(request):
    if request.method == 'POST':
        form = CreatePostForm(request.POST)
        if form.is_valid():
            Post = form.save(commit=False)
            if request.user.is_authenticated():
                Post.autor = request.user
            Post.save()
            cache.delete(MEMCACHE_Post)
    return HttpResponseRedirect('/blog/')

def create_new_user(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            # user must be active for login to work
            user.is_active = True
            user.save()
            return HttpResponseRedirect('/blog/')
    else:
        form = UserCreationForm()
    return direct_to_template(request, 'blog/user_create_form.html',
        {'form': form})
