from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import  UserTask
from django.forms import ModelForm


class SignupForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username','email']
        labels = {'email': 'Email'}


class UserTaskForm(ModelForm):
    class Meta:
        model = UserTask
        fields = ('task_name','created', 'deadline', 'status')



        