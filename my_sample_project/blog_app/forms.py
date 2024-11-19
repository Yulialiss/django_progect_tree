from .models import Comment
from django import forms
from .models import BlogPost

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['user', 'text']


class EmailForm(forms.Form):
    to_email = forms.EmailField(label="Recipient Email")
    subject = forms.CharField(max_length=255, label="Subject")
    text = forms.CharField(widget=forms.Textarea, label="Message")

class BlogPostForm(forms.ModelForm):
    class Meta:
        model = BlogPost
        fields = ['title', 'text', 'image', 'status']

    def clean_status(self):
        status = self.cleaned_data.get('status')
        if status not in dict(BlogPost.PostStatus.choices):
            raise forms.ValidationError("Невірний статус")
        return status


class TagSearchForm(forms.Form):
    tag = forms.CharField(max_length=100, required=True, label="Тег")
