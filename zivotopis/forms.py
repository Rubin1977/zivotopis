from django import forms
from .models import Post
from .models import Email

class PostForm(forms.ModelForm):

    class Meta:
        model = Post
        fields = ('title', 'text',)
        

class EmailForm(forms.ModelForm):
    class Meta:
        model = Email
        fields = ('sender_name', 'sender_email', 'subject', 'message', )
