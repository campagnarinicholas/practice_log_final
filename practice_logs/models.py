from django.db import models
from django.contrib.auth.models import User
from datetime import datetime
from django.db.models.signals import pre_save

# Create your models here.

class Profile(models.Model):
	user = models.OneToOneField(User, null=True, on_delete=models.CASCADE)
	name = models.CharField(max_length=200, null=True)

	def save(self, *args, **kwargs):
		if self.skill_selected != None:
			super(Profile, self).save(*args, **kwargs)

		else:
			super(Profile, self).save(*args, **kwargs)

	def __str__(self):
		return str(self.name)

class Skill(models.Model):
	name = models.CharField(max_length=200, null=False)
	hours = models.IntegerField(null=False, default=0)
	user = models.ForeignKey(User, null=-True, on_delete=models.CASCADE)

	def __str__(self):
		return self.name

class Skill_Entry(models.Model):
	description = models.CharField(max_length=2000, null=True)
	user = models.ForeignKey(User, null=-True, on_delete=models.CASCADE)
	date_added = models.DateTimeField(auto_now_add=True)
	hours_practiced = models.IntegerField(null=False, default=0)
	skill = models.ForeignKey(Skill, null=-True, on_delete=models.CASCADE)

	def __str__(self):
		return str(self.skill)
