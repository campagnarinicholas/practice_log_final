from django.urls import path

from django.contrib.auth import views as auth_views

from . import views

urlpatterns = [
	path('', views.home, name="home"),
	path('create_skill/', views.createSkill, name='create_skill'),
	path('skill_entry/', views.new_time, name='skill_entry'),

	path('register/', views.registerPage, name='register'),
	path('login/', views.loginPage, name='login'),
	path('logout/', views.logoutUser, name='logout'),

	path('delete_all/', views.deleteSkill_Entries, name='delete_all'),
	path('delete_skill/<str:pk>/', views.deleteSkill, name='delete_skill')

	]