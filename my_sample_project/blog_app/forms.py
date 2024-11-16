from .models import Comment
from django import forms

class ContactForm(forms.Form):
    name = forms.CharField(max_length=100, required=True, label="Ваше ім'я")
    email = forms.EmailField(required=True, label="Ваша електронна пошта")
    message = forms.CharField(widget=forms.Textarea, required=True, label="Ваше повідомлення")


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['user', 'text']