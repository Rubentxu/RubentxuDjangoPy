from django import forms 
from blog.models import   Categoria ,Post

class CategoriaForm(forms.ModelForm):
    class Meta:
        model= Categoria
        

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        exclude = ['autor']       
        

