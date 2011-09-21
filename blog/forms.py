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
        
class Post_TagForm(forms.ModelForm):
    class Meta:
        model= Post_Tag
                