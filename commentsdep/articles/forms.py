from django.forms import ModelForm
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Comment


class CommentAddForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = [
            'content',
        ]


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