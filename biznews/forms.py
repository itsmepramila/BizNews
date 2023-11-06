from django import forms
from biznews.models import Post, Category, Tag, Contact, Newsletter

class ContactForm(forms.ModelForm):
    class Meta:
        model=Contact
        fields="__all__"
        
class CommentForm(forms.ModelForm):
    class Meta:
        model=Contact
        fields="__all__"
        
class NewsletterForm(forms.ModelForm):
    class Meta:
        model=Newsletter
        fields="__all__"
    