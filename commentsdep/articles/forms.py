from django.forms import ModelForm
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Comment, Article, Profile
from django.core.exceptions import ValidationError 


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

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['content'].widget.attrs.update({
            'class': 'form-input',
            'rows': 5,
            })
        self.fields['content'].required=False


    def clean(self):
        print("CLEAN: ", self.cleaned_data)
        content = self.cleaned_data['content']
        if not content:
            self.add_error('content', 'Komentarz pusty!') 


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


class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['image']
