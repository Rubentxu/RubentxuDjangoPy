from django.db import models
from django.contrib.auth.models import User
from markdown import markdown
from django.template.defaultfilters import slugify
import datetime ,re ,logging
from djangotoolbox.fields import ListField ,EmbeddedModelField
from django import forms


log = logging.getLogger(__name__)

class StringListField(forms.CharField):
    def prepare_value(self, value):
        return ', '.join(value)

    def to_python(self, value):
        if not value:
            return []
        if ',' in value:
            return [tag.strip() for tag in value.split(',')]
        else:
            return [tag.strip() for tag in value.split()]       
    
class TagField(ListField):
    def formfield(self, **kwargs):
        return models.Field.formfield(self, StringListField, **kwargs)




class PostsActivosManager(models.Manager):
    def get_query_set(self):
        return super(PostsActivosManager, self).get_query_set().filter(estado=self.model.ACTIVO)   
    
    def tagCloud(self, lista):
        d=dict()
        tam=0    
        for t in lista:
            for tag in t:
                for t2 in tag:
                    if d.has_key(str(t2)):
                        d[str(t2)]+=1
                        tam+=1
                    else:     
                        d[str(t2)]=1
                        tam+=1
                         
        for a,b in d.items():
            d[a]=b*10/tam                     
        
        return d

class Categoria(models.Model):    
    nombre = models.CharField(max_length=50, unique=True)
    slug= models.SlugField(unique=True,editable=False,help_text="Valor generado automaticamente segun el nombre")
    descripcion = models.TextField()
    
    
    def __unicode__(self):
        return 'Categoria: %s Descripcion: %s' % (self.nombre, self.descripcion)  
    
    def save(self, force_insert=False, force_update= False):        
        if not self.id:
            self.slug= slugify(self.nombre)                
        super(Categoria,self).save(force_insert, force_update)   
    
    @models.permalink
    def get_absolute_url(self):
        return ('categoria_detalle'),(),{'slug': self.slug}
    
    def posts_activos(self):
        return self.post.filter(estado=Post.ACTIVO)
    
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
    
    autor = EmbeddedModelField(User)
    titulo= models.CharField(max_length=50,unique=True)
    contenido = models.TextField()    
    creado = models.DateTimeField(editable=False)
    modificado= models.DateTimeField(editable=False)
    contenido_html= models.TextField(editable=False,blank=True)     
    activa_comentarios= models.BooleanField(default=True)
    slug= models.SlugField(unique=True,editable=False)
    estado= models.IntegerField(choices=ESTADOS_CHOICES, default=ACTIVO)    
    tags =TagField()
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
        def convert_tag(tag):
            tag = tag.strip().lower()
            return re.sub('[^a-z0-9_-]', '', tag)
        self.tags = [convert_tag(tag) for tag in self.tags]
        self.tags = [tag for tag in self.tags if tag.strip()]
        super(Post,self).save(force_insert, force_update)      
    
    class Meta:
        ordering = ["creado"]
        
    @models.permalink
    def get_absolute_url(self):
        return ('blog.views.ver_Post', [str(self.slug)])                  

