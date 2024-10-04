
from django import forms
from .models import Comment, Post
from django.contrib.auth.models import User 
from django.contrib.auth.forms import UserCreationForm 
from django_ckeditor_5.widgets import CKEditor5Widget

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ('title','body','author','category')
    
    # overriding default form setting and adding bootstrap class
    def __init__(self, *args, **kwargs):
        super(PostForm, self).__init__(*args, **kwargs)
        self.fields["title"].required = True
        self.fields["body"].required = True

   

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('name', 'email', 'body')
    
    # overriding default form setting and adding bootstrap class
    def __init__(self, *args, **kwargs):
        super(CommentForm, self).__init__(*args, **kwargs)
        self.fields['name'].widget.attrs = {'placeholder': 'Enter name','class':'form-control'}
        self.fields['email'].widget.attrs = {'placeholder': 'Enter email', 'class':'form-control'}
        self.fields['body'].widget.attrs = {'placeholder': 'Comment here...', 'class':'form-control', 'rows':'5'}

class SignUpForm(UserCreationForm): 
    def __init__(self, *args, **kwargs): 
        super().__init__(*args, **kwargs) 
        self.fields['username'].widget.attrs.update({ 
            'class': 'form-control', 
            'required':'', 
            'name':'username', 
            'id':'username', 
            'type':'text', 
            'placeholder':'John Doe', 
            'maxlength': '16', 
            'minlength': '6', 
            }) 
        self.fields['email'].widget.attrs.update({ 
            'class': 'form-control', 
            'required':'', 
            'name':'email', 
            'id':'email', 
            'type':'email', 
            'placeholder':'JohnDoe@mail.com', 
            }) 
        self.fields['password1'].widget.attrs.update({ 
            'class': 'form-control', 
            'required':'', 
            'name':'password1', 
            'id':'password1', 
            'type':'password', 
            'placeholder':'*****', 
            'maxlength':'22',  
            'minlength':'8' 
            }) 
        self.fields['password2'].widget.attrs.update({ 
            'class': 'form-control', 
            'required':'', 
            'name':'password2', 
            'id':'password2', 
            'type':'password', 
            'placeholder':'*****', 
            'maxlength':'22',  
            'minlength':'8' 
            }) 
 
 
    username = forms.CharField(max_length=20, label=False) 
    email = forms.EmailField(max_length=100) 
 
    class Meta: 
        model = User 
        fields = ('username', 'email', 'password1', 'password2', ) 
   