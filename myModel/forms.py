from django import forms
from .models import *
  
class StereoImgForm(forms.ModelForm):
  
    class Meta:
        model = StereoImages
        fields = ('StereoImg',)