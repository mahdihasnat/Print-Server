from django.db import models
from django.contrib.auth.models import AbstractBaseUser,PermissionsMixin,AbstractUser
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.contrib.auth.models import UserManager

class TeamUser(AbstractBaseUser):
	"""
		username and password are required. Other fields are optional.
	"""
	username_validator = UnicodeUsernameValidator()

	username = models.CharField(
        max_length=150,
        unique=True,
        help_text=(
            "Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only."
        ),
        validators=[username_validator],
        error_messages={
            "unique": "A user with that username already exists.",
        },
  )
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

	objects = UserManager()

	USERNAME_FIELD = 'username'
	REQUIRED_FIELDS = [] #['team_name','location']
