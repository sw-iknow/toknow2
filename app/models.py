from django.db import models
from django.contrib.auth.models import User

class UserInfo(models.Model):
    message = models.CharField(max_length=200)
    authuser_id = models.ForeignKey(User)

class SkillType(models.Model):
	level = models.IntegerField()
	parent_id = models.ForeignKey("self", null=True)
	name = models.CharField(max_length=200)
	url = models.CharField(max_length=200)

class SkillInstance(models.Model):
	user_id = models.ForeignKey(UserInfo)
	skill_type_id = models.ForeignKey(SkillType)
	instance_type = models.CharField(max_length=30)
	snippet = models.CharField(max_length=200)

class Hookup(models.Model):
	requester_id = models.ForeignKey(UserInfo, related_name='requester_hookups')
	offerer_id = models.ForeignKey(UserInfo, related_name='offerer_hookups')
	rating = models.IntegerField()
	date = models.DateField()

