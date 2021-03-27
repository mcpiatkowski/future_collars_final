from django.forms import ModelForm
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Comment, Article


class ArticleCreateForm(forms.ModelForm):
    class Meta:
        model = Article
        fields = [
            'title',
            'content',
            'snippet',
        ]

        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-input'}),
            'content': forms.Textarea(attrs={'class': 'form-input'}),
            'snippet': forms.TextInput(attrs={'class': 'form-input'})
        }


class CommentCreateForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = [
            'content',
            ]

        widgets = {
            'content': forms.Textarea(attrs={
                'class': 'form-input',
                'rows': 10,
                'novalidate': 'True'
                })
            }


class CommentForm(forms.Form):
    comment = forms.CharField(widget=forms.Textarea(attrs={
        'class': 'form-input',
        'placeholder': 'Your Comment',
        'rows': 5,
    }))


class CreateUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = [
            'username',
            'email',
            'password1',
            'password2',
        ]