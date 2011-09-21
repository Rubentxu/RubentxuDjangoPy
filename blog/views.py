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

logger = logging.getLogger(__name__)

def mark(request):
    logger.debug('Hemos entrado en mi vista: markdown')
    data= request.POST.get('data')    
    return HttpResponse(markdown(data)) 

@cache_page(60 * 1)
def index_Posts(request, pagina):
    logger.debug('Hemos entrado en mi_vista: index_Posts')
    cat=Categoria.objects.all()                                              
    tag= Tag.objects.all()
    tam= tag.count()
    logger.debug('Tamanyo: '+ str(tam))    
    tags= dict([(t.etiqueta,int(tam/t.post_tag_set.all().count()) ) for t in tag])   
       
    logger.debug(' Nube Tags: '+str(tags))      
    pagina= int(pagina)
    inicio=  5*(pagina-1)    
    fin=   (5*pagina)   
    cantidad= Post.activo.all().count()                 
    logger.debug('Inicio: '+ str(inicio)+ ' Fin: '+ str(fin)+' Pagina: '+ str(pagina)+'Cantidad : '+ str(cantidad))
    Posts = Post.activo.all().order_by('-creado')[inicio:fin]        
    logger.debug(Posts)       
              
    atras=pagina-1 if inicio>1 else pagina
    sig=pagina+1 if fin<cantidad else pagina    
        
    return direct_to_template(request, 'blog/index.html',
                              {'Posts': Posts,
                               'atras': atras,
                               'sig':sig,
                               'pag':pagina,
                               'cat':cat,
                               'tags':tags})

@login_required( login_url='/accounts/login/')
@staff_member_required
def lista_Posts(request):
    logger.debug('Hemos entrado en mi_vista: lista_Posts')           
            
    Posts = Post.objects.all().order_by('-creado')       
    logger.debug(Posts)        
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
                              {'Posts': Posts})
    
@login_required( login_url='/accounts/login/')
@staff_member_required
def crear_Post(request):
    logger.debug('Hemos entrado en mi_vista: crear_Post')   
    pformset= PostForm
    tformset= formset_factory( TagForm, extra=4,can_delete=False)
    
    if request.method == 'POST':
        formset= pformset(request.POST,request.FILES,prefix='post')
        tagformset= tformset(request.POST, request.FILES,prefix='tag')
        logger.debug('Formulario Crear Valido...')
        if formset.is_valid() :                               
                          
            post=formset.save(commit=False)
            post.autor= request.user                            
            post.save() 
            logger.debug('Post: '+ str(post.id))             
            for tag in tagformset:                
                t=tag.save(commit=False)                
                if not (t.etiqueta is None or t.etiqueta==''):                    
                    try:
                        t= Tag.objects.get(etiqueta=t.etiqueta)                                  
                    except Tag.DoesNotExist:
                        t.save()                                                              
                    logger.debug(' Tag id: '+str(t.id))
                    Post_Tag.objects.create(post=post,tag=t)                                                                        
                
            cantidad= Post.activo.all().count()/5                  
            return HttpResponseRedirect('/blog/')
    else:
        formset= pformset(prefix='post')
        tagformset = tformset(prefix='tag')
    return direct_to_template(request, 'blog/post/post_form.html',
        {'form': formset,
         'tform': tagformset})
 

def ver_Post(request, slug):
    logger.debug('Hemos entrado en mi_vista: ver_Post')      
    P= Post.objects.get(slug=slug)    
    return direct_to_template(request,'blog/post/ver_post.html', 
                              {'Post' : P  })
    
@login_required( login_url='/accounts/login/')    
@staff_member_required    
def modificar_Post(request, slug):
    logger.debug('Hemos entrado en mi_vista: modificar_Post')
    inlineForm= inlineformset_factory(Post, Tag, extra=2,can_delete=False)
    
    p= Post.objects.select_related().get(slug=slug)            
        
    if request.method == 'POST':
        formset= PostForm(request.POST,instance=p)
        tagformset= inlineForm(request.POST, request.FILES, instance=p)
        
        if formset.is_valid() and tagformset.is_valid():
            logger.debug('Formulario Modificar Valido...')                   
                          
            post=formset.save(commit=False)
            post.autor= request.user                            
            post.save() 
                         
            for tag in tagformset:
                t=tag.save(commit=False)
                if not (t.etiqueta is None or t.etiqueta==''):
                    t.post= post               
                    t.save(True, True)          
              
            return HttpResponseRedirect('/blog/')
    else:
        formset= PostForm(instance=p)
        tagformset = inlineForm(instance=p)
         
    return direct_to_template(request, 'blog/post/post_form.html',
        {'form': formset,
         'tform': tagformset})
    
@login_required( login_url='/accounts/login/')
@staff_member_required      
def borrar_Post(request, slug):
    logger.debug('Hemos entrado en mi vista: borrar_Post')
    Post.objects.select_related().get(slug=slug).delete()
    
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

@cache_page(60 * 1)
def categoria_detalle(request, slug):
    categoria = get_object_or_404(Categoria, slug=slug)
    return object_list(request, queryset=categoria.posts_activos(), extra_context={
        'categoria': categoria
    })

@cache_page(60 * 1)    
def lista_Post_Tag(request, tag, pagina):   
    logger.debug('Hemos entrado en mi_vista: index_Posts por Tag')
    cat=Categoria.objects.all()                                              
    t2= Tag.objects.all()
    tam= t2.count()
    logger.debug('Tamanyo: '+ str(tam))    
    tags= dict([(t.etiqueta,int(tam/t.post_tag_set.all().count()) ) for t in t2])   
       
    logger.debug(' Nube Tags: '+str(tags))      
    pagina= int(pagina)
    inicio=  5*(pagina-1)    
    fin=   (5*pagina) 
    t3= t2.get(etiqueta=tag)    
    cantidad= t3.post_tag_set.all().count()               
    logger.debug('Inicio: '+ str(inicio)+ ' Fin: '+ str(fin)+' Pagina: '+ str(pagina)+'Cantidad : '+ str(cantidad))
    Posts = t3.post_tag_set.all().order_by('-creado')[inicio:fin]        
    logger.debug(Posts)    
              
    atras=pagina-1 if inicio>1 else pagina
    sig=pagina+1 if fin<cantidad else pagina    
        
    return direct_to_template(request, 'blog/indextag.html',
                              {'Posts': Posts,
                               'atras': atras,
                               'sig':sig,
                               'pag':pagina,
                               'cat':cat,
                               'tags':tags})    

def lista_Post_Categoria(request, catg, pagina):   
    logger.debug('Hemos entrado en mi_vista: index_Posts por Categoria')
    cat=Categoria.objects.all()                                              
    t2= Tag.objects.all()
    tam= t2.count()
    logger.debug('Tamanyo: '+ str(tam))    
    tags= dict([(t.etiqueta,int(tam/t.post_tag_set.all().count()) ) for t in t2])   
       
    logger.debug(' Nube Tags: '+str(tags))      
    pagina= int(pagina)
    inicio=  5*(pagina-1)    
    fin=   (5*pagina) 
    c3= cat.get(nombre=catg)    
    cantidad= c3.post_set.all().count()               
    logger.debug('Inicio: '+ str(inicio)+ ' Fin: '+ str(fin)+' Pagina: '+ str(pagina)+'Cantidad : '+ str(cantidad))
    Posts = c3.post_set.all().order_by('-creado')[inicio:fin]        
    logger.debug(Posts)    
              
    atras=pagina-1 if inicio>1 else pagina
    sig=pagina+1 if fin<cantidad else pagina    
        
    return direct_to_template(request, 'blog/indexcat.html',
                              {'Posts': Posts,
                               'atras': atras,
                               'sig':sig,
                               'pag':pagina,
                               'cat':cat,
                               'tags':tags})    
