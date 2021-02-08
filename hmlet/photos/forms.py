from django import forms
from .models import *


#FORM WHICH HAS THE FIELDS FOR A NEW POST 

class DocumentForm(forms.Form):

    class Meta:
        model=photos
        fields = ['user','image','caption','published_date','tags']