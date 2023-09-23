from django import forms
from .models import Post
from .models import Email
#from captcha.fields import ReCaptchaField
#from captcha.widgets import ReCaptchaV2Checkbox

class PostForm(forms.ModelForm):

    class Meta:
        model = Post
        fields = ('title', 'text',)
        

class EmailForm(forms.ModelForm):
    class Meta:
        model = Email
        fields = ('sender_name', 'sender_email', 'subject', 'message',)
        

#class ContactForm(forms.Form):
#    jmeno = forms.CharField(label='Vaše meno (povinné)', max_length=100)
#    email = forms.EmailField(label='Váš email (povinné)')
#    predmet = forms.CharField(label='Predmet', max_length=80)
#    #rok = forms.IntegerField(label='Aktuálny rok')
#    sprava = forms.CharField(label='Správa', widget=forms.Textarea)
#    #recaptcha = ReCaptchaField()
     #captcha = ReCaptchaField(widget=ReCaptchaV2Checkbox())
    

