from django.db import models
from django.contrib.auth.models import User

class Post(models.Model):
    autor = models.ForeignKey(User, null=True, blank=True)
    titulo= models.CharField(max_length=50,unique=True)
    contenido = models.TextField()
    fecha = models.DateTimeField(auto_now_add=True)
    modificado= models.DateTimeField(auto_now_add=True)  
    
    def __str__(self):
        return 'Titulo: %s Contenido: %s' % (self.titulo, self.contenido)  
    
    class Meta:
        ordering = ["fecha"]
        unique_together= ['titulo','fecha']
    
class Comentario(models.Model):
    post = models.ForeignKey(Post, null=True, blank=True)
    autor = models.ForeignKey(User, null=True, blank=True)
    contenido = models.TextField()
    fecha = models.DateTimeField(auto_now_add=True)
    ip= models.IPAddressField()
    
    def __str__(self):
        return 'Comentario: %s Fecha: %s' % (self.contenido, self.fecha) 
    
    class Meta:
        ordering = ["fecha"] 
               

class Tag(models.Model):
    post = models.ForeignKey(Post, null=True, blank=True)
    nombre = models.CharField(max_length=50, unique=True)
    descripcion = models.TextField()
    
    def __str__(self):
        return 'Etiqueta: %s Descripcion: %s' % (self.nombre, self.descripcion) 
     
    class Meta:
        ordering = ["nombre"]
        unique_together= ['nombre','descripcion']
           
    
class Categoria(models.Model):
    post= models.OneToOneField(Post, null=True, blank=True)
    nombre = models.CharField(max_length=50, unique=True)
    descripcion = models.TextField()
    
    def __str__(self):
        return 'Categoria: %s Descripcion: %s' % (self.nombre, self.descripcion)  
    
    class Meta:
        ordering = ["nombre"]
        unique_together= ['nombre','descripcion']
    
        