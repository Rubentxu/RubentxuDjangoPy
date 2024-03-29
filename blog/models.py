from django.db import models
from django.contrib.auth.models import User
from markdown import markdown
from django.template.defaultfilters import slugify
import datetime


class PostsActivosManager(models.Manager):
    def get_query_set(self):
        return super(PostsActivosManager, self).get_query_set().filter(estado=self.model.ACTIVO)   
   

class Categoria(models.Model):    
    nombre = models.CharField(max_length=50, unique=True)
    slug= models.SlugField(unique=True, help_text="Valor generado automaticamente segun el nombre")
    descripcion = models.TextField()
    
    def __unicode__(self):
        return 'Categoria: %s Descripcion: %s' % (self.nombre, self.descripcion)  
    
    @models.permalink
    def get_absolute_url(self):
        return ('categoria_detalle'),(),{'slug': self.slug}
    
    def posts_activos(self):
        return self.post_set.filter(estado=Post.ACTIVO)
    
    class Meta:
        ordering = ["nombre"]        
        verbose_name_plural= "Categorias"
        
class Post(models.Model):
    
    ACTIVO= 1
    BORRADOR= 2
    OCULTO= 3
    ESTADOS_CHOICES=(
         (ACTIVO, 'Activo'),
         (BORRADOR, 'Borrador'),
         (OCULTO, 'Oculto'),                    
                     )
    
    autor = models.ForeignKey(User)
    titulo= models.CharField(max_length=50,unique=True)
    contenido = models.TextField()    
    creado = models.DateTimeField(editable=False)
    modificado= models.DateTimeField(editable=False)
    contenido_html= models.TextField(editable=False,blank=True)     
    activa_comentarios= models.BooleanField(default=True)
    slug= models.SlugField(unique=True,editable=False)
    estado= models.IntegerField(choices=ESTADOS_CHOICES, default=ACTIVO)
    categoria= models.ForeignKey(Categoria)    
    
    objects= models.Manager()
    activo= PostsActivosManager()
    
    
    def  __unicode__(self):
        return 'Titulo: %s Estado: %s' % (self.titulo, self.estado)
    
    def save(self, force_insert=False, force_update= False):
        self.contenido_html= markdown(self.contenido)
        if not self.id:
            self.slug= slugify(self.titulo)
            self.creado= datetime.datetime.today()
        self.modificado= datetime.datetime.today()            
        super(Post,self).save(force_insert, force_update)      
    
    class Meta:
        ordering = ["creado"]
        
    @models.permalink
    def get_absolute_url(self):
        return ('blog.views.ver_Post', [str(self.slug)])      
                       

class Tag(models.Model):    
    etiqueta = models.CharField(max_length=50)   
    
    def __unicode__(self):
        return 'Etiqueta: %s' % (self.etiqueta) 
     
    class Meta:
        ordering = ["etiqueta"]
        
    
class Post_Tag(models.Model):    
    post = models.ForeignKey(Post)
    tag= models.ForeignKey(Tag)      
    
    def __unicode__(self):
        return 'Post: %s ' % (self.post)    
    