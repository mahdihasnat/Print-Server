from django.db import models
from django.contrib.auth.models import AbstractUser , AbstractBaseUser,PermissionsMixin,UserManager
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.utils.translation import gettext_lazy as _
from django.utils import timezone
from django.core.mail import send_mail
from django.db.models import Sum

class MyUser(AbstractBaseUser, PermissionsMixin):
	"""
	Most of the code copied from Abstract User
	"""
	username_validator = UnicodeUsernameValidator()

	username = models.CharField(
			_("username"),
			primary_key=True,
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
	name = models.CharField(_("first name"), max_length=150, blank=True,null=True)
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
			indexes = [models.Index(fields=['username',])]


	def clean(self):
			super().clean()
			self.email = self.__class__.objects.normalize_email(self.email)

	def get_full_name(self):
			"""
			Return the first_name plus the last_name, with a space in between.
			"""
			full_name = "%s" % (self.name)
			return full_name.strip()

	def get_short_name(self):
			"""Return the short name for the user."""
			return self.name

	def __str__(self):
		return self.get_full_name()+" ("+self.username+")"

	def email_user(self, subject, message, from_email=None, **kwargs):
			"""Send an email to this user."""
			send_mail(subject, message, from_email, [self.email], **kwargs)

	class Meta(AbstractUser.Meta):
		swappable = "AUTH_USER_MODEL"


class Lab(models.Model):
	id = models.BigAutoField(
		auto_created=True, 
		primary_key=True,
		serialize=True,  
		verbose_name='ID'
	)
	name = models.CharField(
		"Lab name",
		max_length=10,
		blank=True,
		null=True,
		unique = True,
		help_text="Lab name"
	)

	def __str__(self) -> str:
		return self.name

class TeamUser(models.Model):
	user = models.OneToOneField(MyUser, on_delete=models.CASCADE,primary_key=True)
	lab = models.ForeignKey(
		Lab,
		on_delete=models.SET_NULL,
		blank=True,
		null=True,
		default=None,
		help_text="Lab"
	)
	location = models.CharField(
		max_length=255,
		blank=True,
		null=True,
		verbose_name='Location',
	)

	class Meta:
		indexes = [models.Index(fields=['user',])]

	def __str__(self):
		return str(self.user)

	def get_name(self):
		return self.user.name
	
	def get_total_page_usage(self):
		"""
			TODO: change to some sql query thing for faster execution
		"""
		cnt = self.prints.aggregate(a=Sum('total_page'))['a']
		if cnt == None:
			cnt=0
		return cnt


class PrinterUser(models.Model):
	user = models.OneToOneField(MyUser, on_delete=models.CASCADE,primary_key=True)