from django import forms  
from django.forms.models import inlineformset_factory
from blog.models import *
import logging

logger = logging.getLogger(__name__)
class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        exclude = ['autor']       
        
    
        
class TagForm(forms.ModelForm):
    class Meta:
        model = Tag
    def clean(self):
        datos= self.cleaned_data
        id= datos.get('id')
        tag= datos.get('etiqueta')
        
        if not (tag is None or tag==''):
            try:
                t= Tag.objects.get(etiqueta=tag)
                datos['id']= t.id
                logger.debug('< Tag id:> '+str(datos.get('id')))
                return datos                       
            except Tag.DoesNotExist:
                logger.debug('< Tag etiqueta:> '+str(tag))
                return datos
                          
        raise forms.ValidationError("Fallo en Validacion de las Etiquetas...!")
        return None    
        
class Post_TagForm(forms.ModelForm):
    class Meta:
        model= Post_Tag
                