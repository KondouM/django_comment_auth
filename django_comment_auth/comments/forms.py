from django import forms
from .models import Comment
from django.contrib.auth.models import User

class CommentForm(forms.ModelForm):
    
    class Meta:
        model =Comment
        fields = ('title','body')
        widgets = {
            'title': forms.TextInput(attrs={
            'class': 'form-control'
            }),
            'body': forms.TextInput(attrs={
            'class': 'form-control'
            }),
        }
        labels = {
            'title': 'タイトル',
            'body': '本文',
        }
    def clean(self):
        data = super().clean()
        title = data.get('title')
        body = data.get('body')
        if title is None:
            msg = "タイトルが入力されていません。"
            self.add_error('title', msg)
        elif len(title) > 10:
            msg = "タイトルの最大文字数は10文字です。"
            self.add_error('title', msg)
        if body is None:
            msg = "本文が入力されていません。"
            self.add_error('body', msg)
        elif len(body) > 20:
            msg = "本文の最大文字数は20文字です。"
            self.add_error('body', msg)


class UserForm(forms.ModelForm):

    class Meta:
        model = User
        fields = ('first_name', 'last_name')
        widgets = {
            'first_name': forms.TextInput(attrs={
                'class': 'form-control'
            }),
            'last_name': forms.TextInput(attrs={
                'class': 'form-control'
            }),
        }
        labels = {
            'first_name': 'First Name',
            'last_name': 'Last Name',
        }
    def clean(self):
        data = super().clean()
        first_name = data.get('first_name')
        last_name = data.get('last_name')
        if first_name is None:
            msg = "First Name が入力されていません"
            self.add_error('first_name', msg)
        elif len(first_name) > 20:
            msg = "First Name の最大文字数は20文字です"
            self.add_error('first_name', msg)
        if last_name is None:
            msg = "Last Name が入力されていません"
            self.add_error('last_name', msg)
        elif len(last_name) > 20:
            msg = "Last Name の最大文字数は20文字です"
            self.add_error('last_name', msg)