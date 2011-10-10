from django.contrib.auth.forms import UserCreationForm
from django.views.generic.simple import direct_to_template
from django.http import HttpResponseRedirect,HttpResponse
from blog.forms import *
from blog.models import *
from django.shortcuts import get_object_or_404
from django.views.generic.list_detail import object_list
import logging
from django.contrib.auth.decorators import login_required 
from django.contrib.admin.views.decorators import staff_member_required
from markdown import markdown
from django.forms.models import formset_factory,inlineformset_factory
from django.core.paginator import Paginator , EmptyPage, PageNotAnInteger
from django.utils.datetime_safe import datetime
from django.db.models import Count
from django.views.decorators.cache import cache_page
from django.core.cache import cache

logger = logging.getLogger(__name__)

def mark(request):
    logger.debug('Hemos entrado en mi vista: markdown')
    data= request.POST.get('data')    
    return HttpResponse(markdown(data)) 

@cache_page(60 * 120)
def index_Posts(request, pagina):
    logger.debug('Hemos entrado en mi_vista: index_Posts')
    
    Cat= Categoria.objects.all()   
    pagina= int(pagina)
    inicio=  5*(pagina-1)    
    fin=   (5*pagina)   
    cantidad= Post.activo.all().count()                 
    logger.debug('Inicio: '+ str(inicio)+ ' Fin: '+ str(fin)+' Pagina: '+ str(pagina)+'Cantidad : '+ str(cantidad))
    Posts = Post.activo.all().order_by('-creado')[inicio:fin]
    cloud= cache.get('nubetags')
    if cloud is None: 
        cloud = Post.activo.tagCloud(list(Post.activo.values_list('tags')))
        cache.set('nubetags', cloud)
        logger.debug(cloud)   
        
           
              
    atras=pagina-1 if inicio>1 else pagina
    sig=pagina+1 if fin<cantidad else pagina    
        
    return direct_to_template(request, 'blog/index.html',
                              {'Posts': Posts,
                               'atras': atras,
                               'sig':sig,
                               'pag':pagina,
                               'cat':Cat,
                               'tags':cloud})

@login_required( login_url='/accounts/login/')
@staff_member_required
def lista_Posts(request):
    logger.debug('Hemos entrado en mi_vista: lista_Posts')           
    Cat= Categoria.objects.all()           
    Posts = Post.objects.all().order_by('-creado')
    cloud= cache.get('nubetags')
    if cloud is None: 
        cloud = Post.activo.tagCloud(list(Post.activo.values_list('tags')))
        cache.set('nubetags', cloud)            
    paginator= Paginator (Posts,5)
    page= request.GET.get('page')
    
    if page is None or page=='':
        page=1
    try:
        Posts= paginator.page(int(page))
    except PageNotAnInteger:
        Posts= paginator.page(1)
    except EmptyPage:
        Posts= paginator.page(paginator.num_pages)       
    return direct_to_template(request, 'blog/post/lista_posts.html',
                              {'Posts': Posts, 'cat':Cat, 'tags':cloud})
    
@login_required( login_url='/accounts/login/')
@staff_member_required
def crear_Post(request):
    logger.debug('Hemos entrado en mi_vista: crear_Post')   
    pformset= PostForm
    cloud= cache.get('nubetags')
    if cloud is None: 
        cloud = Post.activo.tagCloud(list(Post.activo.values_list('tags')))
        cache.set('nubetags', cloud)
    if request.method == 'POST':
        formset= pformset(request.POST,request.FILES,prefix='post')        
        logger.debug('Formulario Crear Valido...')
        if formset.is_valid() :                               
                          
            post=formset.save(commit=False)
            post.autor= request.user                            
            post.save() 
            logger.debug('Post: '+ str(post.id))           
            cache.clear()                  
            return HttpResponseRedirect('/blog/')
    else:
        formset= pformset(prefix='post')
        
    return direct_to_template(request, 'blog/post/post_form.html',
        {'form': formset ,'tags':cloud})
 

def ver_Post(request, slug):
    logger.debug('Hemos entrado en mi_vista: ver_Post')
    Cat= Categoria.objects.all()
    cloud= cache.get('nubetags')
    if cloud is None: 
        cloud = Post.activo.tagCloud(list(Post.activo.values_list('tags')))
        cache.set('nubetags', cloud)       
    P= Post.objects.get(slug=slug)    
    return direct_to_template(request,'blog/post/ver_post.html', 
                              {'Post' : P,
                               'cat':Cat,
                               'tags':cloud})
    
@login_required( login_url='/accounts/login/')    
@staff_member_required    
def modificar_Post(request, slug):
    logger.debug('Hemos entrado en mi_vista: modificar_Post')
    pformset= PostForm    
    cat=Categoria.objects.all()            
    p= Post.objects.all().get(slug=slug)            
    cloud= cache.get('nubetags')
    if cloud is None: 
        cloud = Post.activo.tagCloud(list(Post.activo.values_list('tags')))
        cache.set('nubetags', cloud)
    if request.method == 'POST':
        formset= pformset(request.POST,instance=p,prefix='post')       
        
        if formset.is_valid() :
            logger.debug('Formulario Modificar Valido...')                   
                          
            post=formset.save(commit=False)
            post.autor= request.user                            
            post.save()            
            cache.clear()  
            return HttpResponseRedirect('/blog/')
    else:
        formset= pformset(instance=p,prefix='post')        
                 
    return direct_to_template(request, 'blog/post/post_form.html',
        {'form': formset, 'cat':cat ,'tags':cloud})
    
@login_required( login_url='/accounts/login/')
@staff_member_required      
def borrar_Post(request, slug):
    logger.debug('Hemos entrado en mi vista: borrar_Post')
    Post.objects.all().get(slug=slug).delete()
    cache.clear()
    return HttpResponseRedirect('/blog/')    

@login_required( login_url='/accounts/login/')
@staff_member_required      
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

@cache_page(60 * 120)
def categoria_detalle(request, slug):
    categoria = get_object_or_404(Categoria, slug=slug)
    return object_list(request, queryset=categoria.posts_activos(), extra_context={
        'categoria': categoria
    })

@cache_page(60 * 120)    
def lista_Post_Tag(request, tag, pagina):   
    logger.debug('Hemos entrado en mi_vista: index_Posts por Tag')
    Posts=Post.activo.filter(tags=tag)
    cat=Categoria.objects.all()
    cloud= cache.get('nubetags')
    if cloud is None: 
        cloud = Post.activo.tagCloud(list(Post.activo.values_list('tags')))
        cache.set('nubetags', cloud)
        logger.debug(cloud)
    cantidad= Post.activo.filter(tags=tag).count()
    logger.debug('Cantidad: '+str(cantidad))
    pagina= int(pagina)
    inicio=  5*(pagina-1)    
    fin=   (5*pagina)               
    atras=pagina-1 if inicio>1 else pagina   
    sig=pagina+1 if fin<cantidad else pagina
        
    return direct_to_template(request, 'blog/indextag.html',
                              {'Posts': Posts,'atras': atras,'sig':sig,'pag':pagina,'cat':cat,'tags':cloud,'tagpag':tag})    
@cache_page(60 * 120)
def lista_Post_Categoria(request, catg, pagina):   
    logger.debug('Hemos entrado en mi_vista: index_Posts por Categoria')
    cat=Categoria.objects.all()
    cloud= cache.get('nubetags')
    if cloud is None: 
        cloud = Post.activo.tagCloud(list(Post.activo.values_list('tags')))
        cache.set('nubetags', cloud)
        logger.debug(cloud)
    pagina= int(pagina)
    inicio=  5*(pagina-1)    
    fin=   (5*pagina) 
    c3= cat.get(nombre=catg)    
    cantidad= c3.post_set.all().count()               
    logger.debug('Inicio: '+ str(inicio)+ ' Fin: '+ str(fin)+' Pagina: '+ str(pagina)+'Cantidad : '+ str(cantidad))
    Posts = c3.post_set.all().order_by('-creado')[inicio:fin]        
       
              
    atras=pagina-1 if inicio>1 else pagina
    sig=pagina+1 if fin<cantidad else pagina    
        
    return direct_to_template(request, 'blog/indexcat.html',
                              {'Posts': Posts,
                               'atras': atras,
                               'sig':sig,
                               'pag':pagina,
                               'cat':cat,
                               'tags':cloud,
                               'catpag':catg})    
