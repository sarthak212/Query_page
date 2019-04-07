from django import forms
from cloneapp.models import user_info,question,answerclass
from django.contrib.auth.models import User

class userprofile(forms.ModelForm):
    class Meta():
        model=User
        fields=['username','email','password']
        widgets={
        'password':forms.PasswordInput(),
        }

class registration_form(forms.ModelForm):
    class Meta():
        model=user_info
        fields=['studies','home','work','image_field']




class new_question_form(forms.ModelForm):
    class Meta():
        model=question
        fields=['question_title']

class answer_form(forms.ModelForm):
    class Meta():
        model=answerclass
        fields=['title_ans']
