from django.core.cache import cache
from django.contrib.auth.forms import UserCreationForm
from django.views.generic.simple import direct_to_template
from django.http import HttpResponseRedirect,HttpResponse
from blog.forms import CreatePostForm ,TagForm
from blog.models import *
from django.shortcuts import get_object_or_404
from django.views.generic.list_detail import object_list
import logging
from django.contrib.auth.decorators import login_required 
from django.contrib.admin.views.decorators import staff_member_required
from markdown import markdown
from django.forms.models import formset_factory


logger = logging.getLogger(__name__)
MEMCACHE_Post = 'Post'
MEMCACHE_listPost = 'listPost'


def mark(request):
    logger.debug('Hemos entrado en mi vista: markdown')
    data= request.POST.get('data')    
    return HttpResponse(markdown(data)) 


def index_Posts(request):
    logger.debug('Hemos entrado en mi_vista: index_Posts')
    Posts = cache.get(MEMCACHE_Post)
    if Posts is None:
        Posts = Post.activo.all().order_by('-creado')[:10]
        logger.debug(Posts)
        cache.add(MEMCACHE_Post, Posts)
    return direct_to_template(request, 'blog/index.html',
                              {'Posts': Posts})

@login_required( login_url='/accounts/login/')
@staff_member_required
def lista_Posts(request):
    logger.debug('Hemos entrado en mi_vista: lista_Posts')
    Posts = cache.get(MEMCACHE_listPost)
    if Posts is None:
        Posts = Post.objects.all().order_by('-creado')[:10]
        logger.debug(Posts)
        cache.add(MEMCACHE_listPost, Posts)
    return direct_to_template(request, 'blog/post/lista_posts.html',
                              {'Posts': Posts})
    
@login_required( login_url='/accounts/login/')
@staff_member_required
def crear_Post(request):
    logger.debug('Hemos entrado en mi_vista: crear_Post')
    PostFormSet= formset_factory(CreatePostForm)
    TagFormSet= formset_factory(TagForm,extra=4)
    
    if request.method == 'POST':
        formset = PostFormSet(request.POST ,prefix='post')
        tagformset= TagFormSet(request.POST, prefix='tag')       
        
        if formset.is_valid() and tagformset.is_valid():
            logger.debug('Formulario Crear Valido...')
                   
            for instance in formset:                
                post=instance.save(commit=False)
                post.autor= request.user                            
                post.save()
                
            for tag in tagformset:
                t=tag.save(commit=False)
                t.post= formset[0].save(commit=False)                
                t.save()
                
            cache.delete(MEMCACHE_Post)
            cache.delete(MEMCACHE_listPost)
            return HttpResponseRedirect('/blog/')
    else:
        formset = PostFormSet(prefix='post')
        tagformset= TagFormSet(prefix='tag')   
    return direct_to_template(request, 'blog/post/post_form.html',
        {'form': formset,
         'tform': tagformset})
 

def ver_Post(request, clave):
    logger.debug('Hemos entrado en mi_vista: ver_Post')      
    P= Post.objects.get(pk=clave)    
    return direct_to_template(request,'blog/post/ver_post.html', 
                              {'Post' : P  })
    
@login_required( login_url='/accounts/login/')    
@staff_member_required    
def modificar_Post(request, clave):
    logger.debug('Hemos entrado en mi_vista: modificar_Post')    
    p=Post.objects.get(pk=clave)
    logger.debug(p)
    if request.method == 'POST':
        form = CreatePostForm(request.POST,instance=p)
        if form.is_valid():
            form.save()            
            cache.delete(MEMCACHE_Post)
            cache.delete(MEMCACHE_listPost)
            return HttpResponseRedirect('/blog/')
    else:
        form = CreatePostForm(instance=p)
    return direct_to_template(request, 'blog/post/post_form.html',
        {'form': form})
    
@login_required( login_url='/accounts/login/')
@staff_member_required      
def borrar_Post(request, clave):
    logger.debug('Hemos entrado en mi vista: borrar_Post')
    Post.objects.get(pk=clave).delete()
    cache.delete(MEMCACHE_Post)
    cache.delete(MEMCACHE_listPost)
    return HttpResponseRedirect('/blog/')    

@login_required( login_url='/accounts/login/')
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


def categoria_detalle(request, slug):
    categoria = get_object_or_404(Categoria, slug=slug)
    return object_list(request, queryset=categoria.posts_activos(), extra_context={
        'categoria': categoria
    })
