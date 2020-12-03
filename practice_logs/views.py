from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.forms import inlineformset_factory
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django import forms
from django.contrib.auth import authenticate, login, logout
from django.views.generic.edit import CreateView
from django.db.models import Sum, Max, Avg
# Create your views here.
from django.contrib.auth.decorators import login_required
from .models import * 
from .forms import CreateUserForm, SkillForm, SkillEntryForm
from .decorators import unauthenticated_user, allowed_users, admin_only
from datetime import *
from django.utils import timezone

@unauthenticated_user
def registerPage(request):
	"""
	Renders our register page
	Uses CreateUserForm from .forms
	Checks if user submitted info is valid, then saves it if it is
	Creates context with key, value for our form
	returns render from register page off template at 'practice_logs/register.html'
	and our context dict
	"""
	form = CreateUserForm

	if request.method == 'POST':
		form = CreateUserForm(request.POST)
		if form.is_valid():
			form.save()
			user = form.cleaned_data.get('username')

			messages.success(request, 'Account was created for ' + user)
			return redirect('login')

	context = {'form':form}
	return render(request, 'practice_logs/register.html', context)

@unauthenticated_user
def loginPage(request):
	"""
	Renders our login page
	Prompts user for username and password, then authenticates provided info
	If user info is accurate, it redirects to home page
	If not, display message saying "Username OR password is incorrect"
	Logging in allows user to access pages with decorator @login_required
	returns page render from template 'practice_logs/login.html'
	"""
	if request.method == 'POST':
		username = request.POST.get('username')
		password = request.POST.get('password')

		user = authenticate(request, username=username, password=password)

		if user is not None:
			login(request, user)
			return redirect('home')
		else:
			messages.info(request, 'Username OR password is incorrect')

	context = {}
	return render(request, 'practice_logs/login.html', context)

def logoutUser(request):
	"""
	Logs user out
	Redirects user to login page when done
	"""
	logout(request)
	return redirect('login')

@login_required(login_url='login')
def home(request):
	"""
	Renders our home pag with information about user's skills
	Gets users skills, skill entries, and profile
	Creates skill_hours_dict for # of hours user inputs for each skill
	Creates avg_hours_daily for average daily hours spent practicing
	Creates max_skill for user's skill that has the most hours inputted this week
	Creates avg_hours for average length of practice session
	Context dict creates keys and values for these variables for our template
	Renders home page with template 'practice_logs/dashboard' with context dict
	"""
	skills = request.user.skill_set.all()
	skill_entry = request.user.skill_entry_set.all()
	profile = Profile.objects.all()

	skill_hours_dict = {}
	for skill in skills:
		skill_hours = skill_entry.filter(skill=skill,
								date_added__range = [datetime.now()-timedelta(days=7), datetime.now()])
		skill_hours_all = skill_hours.aggregate(Sum('hours_practiced'))
		skill_hours_dict[skill] = skill_hours_all['hours_practiced__sum']

	weekly_skill_sessions = skill_entry.filter(
			date_added__range = [datetime.now()-timedelta(days=7), datetime.now()])
	total_skill_hours_weekly = weekly_skill_sessions.aggregate(Sum('hours_practiced')) or 0
	avg_hours_weekly = 0
	if total_skill_hours_weekly['hours_practiced__sum'] != None:
		avg_hours_weekly = round(((total_skill_hours_weekly['hours_practiced__sum']) / 7), 2)

	max_skill_hours = skill_entry.aggregate(Max('hours_practiced')) or 0
	max_skill = Skill_Entry.objects.filter(hours_practiced = max_skill_hours['hours_practiced__max']) or [0]
	avg_hours = skill_entry.aggregate(Avg('hours_practiced')) or 0

	context = {
		'skills':skills, 'skill_entry':skill_entry, 'profile':profile, 
		'avg_hours_weekly':avg_hours_weekly,'max_skill':max_skill[0], 
		'avg_hours':avg_hours['hours_practiced__avg'],
	    'total_skill_hours_weekly':total_skill_hours_weekly['hours_practiced__sum'],
		'skill_hours_dict':skill_hours_dict
		}

	return render(request, 'practice_logs/dashboard.html', context)

@login_required(login_url='login')
def createSkill(request):
	"""
	Create a new skill that we can then create practice sessions for
	Uses SkillForm() from our forms.py
	Takes POST data from user to fill our skill form
	If it is validated, the skill is saved
	Context dict is created so form can be rendered
	returns render of template 'practice_logs/create_skill.html'
	""" 
	skill = Skill(user=request.user)
	form = SkillForm()

	if request.method == "POST":
		form = SkillForm(request.POST)
		if form.is_valid():
			skill = form.save(commit=False)
			skill.user = request.user
			skill.save()
			return redirect('/')

	context = {'form':form}
	return render(request, 'practice_logs/create_skill.html', context)

@login_required(login_url='login')
def new_time(request):
	"""
	Creates a new practice session where user can enter in the skill they practiced,
	hours practiced, and a brief description of their session
	Uses SkillEntryForm() from forms.py
	Takes user's POST data to fill out form
	If form is validated, the practice session is saved (called skill_entry)
	Creates context dict so form can be rendered
	returns render of template at 'practice_logs/skill_entry.html'
	"""
	skill_entry = Skill_Entry(user=request.user)
	form = SkillEntryForm()
	form.fields['skill'].queryset = request.user.skill_set.all()

	if request.method == "POST":
		form = SkillEntryForm(request.POST)
		if form.is_valid():
			skill_entry = form.save(commit=False)
			skill_entry.user = request.user
			skill_entry.save()
			return redirect('/')

	context = {'form':form}
	return render(request, 'practice_logs/skill_entry.html', context)

@login_required(login_url='login')
def deleteSkill_Entries(request):
	"""
	Deletes all user's skill_entries to clear pratice sessions
	Users POST data to delete skill entries
	Creates context dict so entries can be removed
	returns render of template 'practice_logs.delete_all.html' where user is 
	prompted to verify before they delete all entries
	"""
	skill_entries = request.user.skill_entry_set.all()

	if request.method == "POST":
		skill_entries.delete()
		return redirect("/")

	context = {'item':skill_entries}
	return render(request, 'practice_logs/delete_all.html')

@login_required(login_url='login')
def deleteSkill(request, pk):
	"""
	Deletes specific skill from user 
	Uses POST data to delete skill
	Creates context dict so specific skill gets removed
	returns render of template at 'practice_logs/delete_skill.html'
	where user is prompted to verify before they delete entry
	"""
	skill = Skill.objects.get(id=pk)

	if request.method == "POST":
		skill.delete()
		return redirect("/")

	context = {'item':skill}
	return render(request, 'practice_logs/delete_skill.html', context)