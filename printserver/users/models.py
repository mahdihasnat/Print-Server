from django.db import models
from django.contrib.auth.models import AbstractUser , AbstractBaseUser,PermissionsMixin,UserManager
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.utils.translation import gettext_lazy as _
from django.utils import timezone

class MyUser(AbstractBaseUser, PermissionsMixin):
	"""
	Most of the code copied from Abstract User
	"""
	username_validator = UnicodeUsernameValidator()

	username = models.CharField(
			_("username"),
			max_length=150,
			unique=True,
			help_text=_(
					"Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only."
			),
			validators=[username_validator],
			error_messages={
					"unique": _("A user with that username already exists."),
			},
	)
	first_name = models.CharField(_("first name"), max_length=150, blank=True)
	email = models.EmailField(_("email address"), blank=True)
	is_staff = models.BooleanField(
			_("staff status"),
			default=False,
			help_text=_("Designates whether the user can log into this admin site."),
	)
	is_active = models.BooleanField(
			_("active"),
			default=True,
			help_text=_(
					"Designates whether this user should be treated as active. "
					"Unselect this instead of deleting accounts."
			),
	)
	date_joined = models.DateTimeField(_("date joined"), default=timezone.now)
	
	# User defined
	is_team = models.BooleanField(default=False)
	is_printer = models.BooleanField(default=False)

	objects = UserManager()

	EMAIL_FIELD = "email"
	USERNAME_FIELD = "username"
	REQUIRED_FIELDS = ["email"]

	class Meta:
			verbose_name = _("user")
			verbose_name_plural = _("users")
			abstract = True

	def clean(self):
			super().clean()
			self.email = self.__class__.objects.normalize_email(self.email)

	def get_full_name(self):
			"""
			Return the first_name plus the last_name, with a space in between.
			"""
			full_name = "%s" % (self.first_name)
			return full_name.strip()

	def get_short_name(self):
			"""Return the short name for the user."""
			return self.first_name

	def email_user(self, subject, message, from_email=None, **kwargs):
			"""Send an email to this user."""
			send_mail(subject, message, from_email, [self.email], **kwargs)

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