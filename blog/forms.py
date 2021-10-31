from django.forms import models
from blog.models import comment
from django import forms
from  . models import comment

class commentForm(forms.ModelForm):
    class Meta:
      model = comment
      exclude = ["post"]
      labels = {
            "user_name" : "Your Name",
            "user_mail" : "Your Mail",
            "text" : "Comment Here"
      }
