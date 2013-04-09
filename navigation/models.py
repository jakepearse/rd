from django import forms

class ContactForm(forms.Form):
  name = forms.CharField(max_length=100)
  subject = forms.CharField(required=False)
  message = forms.CharField(required=True)
  sender = forms.EmailField(required=True)
  email_copy = forms.BooleanField(required=False)
  def __unicode__(self):
    return self.title