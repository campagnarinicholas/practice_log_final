from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms

from .models import *

class CreateUserForm(UserCreationForm):
	class Meta:
		model = User
		fields = ['username', 'email', 'first_name', 'last_name', 'password1', 'password2']

class SkillForm(forms.ModelForm):
	class Meta:
		model = Skill
		fields = ['name']

class SkillEntryForm(forms.ModelForm):
	class Meta:
		model = Skill_Entry
		fields = ['skill', 'hours_practiced', 'description']