from django import forms
from .models import Comment


class EmailPostForm(forms.Form):
    name = forms.CharField( max_length=25)
    from_email = forms.EmailField()
    to_email = forms.EmailField()
    comments = forms.CharField(widget=forms.Textarea, max_length=250, required=False)



class CommentForm(forms.ModelForm):
    

    class Meta:
        model = Comment
        fields = ('name', 'email', 'body',)


class SearchForm(forms.Form):
    query = forms.CharField(max_length=255)