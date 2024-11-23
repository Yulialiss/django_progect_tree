from .models import Comment
from django import forms
from .models import BlogPost
from taggit.forms import TagField

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['user', 'text']


class EmailForm(forms.Form):
    to_email = forms.EmailField(label="Recipient Email")
    subject = forms.CharField(max_length=255, label="Subject")
    text = forms.CharField(widget=forms.Textarea, label="Message")

class BlogPostForm(forms.ModelForm):
    tags = TagField(required=False)

    class Meta:
        model = BlogPost
        fields = ['title', 'text', 'image', 'status','tags']

    def clean_status(self):
        status = self.cleaned_data.get('status')
        if status not in dict(BlogPost.PostStatus.choices):
            raise forms.ValidationError("Невірний статус")
        return status


class TagSearchForm(forms.Form):
    tag = forms.CharField(max_length=100, required=True, label="Тег")


class EmailForm(forms.Form):
    subject = forms.CharField(max_length=100, label="Тема", widget=forms.TextInput(attrs={"class": "form-control"}))
    message = forms.CharField(label="Повідомлення", widget=forms.Textarea(attrs={"class": "form-control"}))
    recipient = forms.EmailField(label="Отримувач", widget=forms.EmailInput(attrs={"class": "form-control"}))