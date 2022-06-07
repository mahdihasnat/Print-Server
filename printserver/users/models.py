from django.db import models
from django.contrib.auth.models import AbstractUser

class MyUser(AbstractUser):
	is_team = models.BooleanField(default=False)
	is_printer = models.BooleanField(default=False)

	class Meta(AbstractUser.Meta):
		swappable = "AUTH_USER_MODEL"

class TeamUser(models.Model):
	user = models.OneToOneField(MyUser, on_delete=models.CASCADE,primary_key=True)
	team_name = models.CharField(
		max_length=255,
		blank=True,
		null=True,
		verbose_name='Team Name',
	)
	location = models.CharField(
		max_length=255,
		blank=True,
		null=True,
		verbose_name='Location',
	)

	def __str__(self):
		return self.team_name

class PrinterUser(models.Model):
	user = models.OneToOneField(MyUser, on_delete=models.CASCADE,primary_key=True)