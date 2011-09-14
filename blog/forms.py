from django import forms
from blog.models import Post ,Tag

class CreatePostForm(forms.ModelForm):
    class Meta:
        model = Post
        exclude = ['autor']       
        
    
        
class TagForm(forms.ModelForm):
    class Meta:
        model = Tag
        exclude = ['post']        