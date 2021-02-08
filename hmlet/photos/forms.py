from django import forms
from .models import *


# class DocumentForm(forms.Form):
#     docfile = forms.FileField(label='Select a file',)

class DocumentForm(forms.Form):

    class Meta:
        model=photos
        fields = ['user','image','caption','published_date','tags']