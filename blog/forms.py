from django import forms  
from django.forms.models import inlineformset_factory
from blog.models import Post ,Tag, Categoria

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        exclude = ['autor']       
        
    
        
class TagForm(forms.ModelForm):
    class Meta:
        model = Tag
        exclude = ['post']      
        
postInline= inlineformset_factory(Post, Tag)          