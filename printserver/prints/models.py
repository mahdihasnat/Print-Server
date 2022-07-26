from django.db import models
from solo.models import SingletonModel

class Prints(models.Model):

	class Status(models.IntegerChoices):
		QUEUED = 1
		PRINTING = 2
		DELIVERED = 3

	print_id = models.AutoField(primary_key=True)
	owner = models.ForeignKey('users.TeamUser', on_delete=models.CASCADE , related_name='prints')
	source_code = models.TextField()

	submission_time = models.DateTimeField(auto_now_add=True)
	printing_time = models.DateTimeField(null=True,blank=True)

	total_page = models.IntegerField(null=True,blank=True)
	status = models.IntegerField(choices=Status.choices, default=Status.QUEUED)


class PrintConfiguration(SingletonModel):

	class PaperType(models.TextChoices):
		A3 = 'A3'
		A4 = 'A4'
		A5 = 'A5'
		Letter = 'Letter'
		Legal = 'Legal'

	paper_type = models.CharField(choices=PaperType.choices, max_length=10, default=PaperType.A4)
	

	class Orientation(models.TextChoices):
		Portrait = 'P'
		Landscape = 'L'
	
	orientation = models.CharField(choices=Orientation.choices, max_length=1, default=Orientation.Portrait)


	class UserUnit(models.TextChoices):
		Point = 'pt'
		Millimeter = 'mm'
		Centimeter = 'cm'
		Inch = 'in'

	unit = models.CharField(choices=UserUnit.choices, max_length=2, default=UserUnit.Point)


	line_height = models.FloatField(
		default=12.0,
		null=False,
		blank=False,
		verbose_name="Line Height in Units",
		help_text="Default: 12.0 (in Points)"
	)
	
	font_size = models.FloatField(
		default=11.0,
		null=False,
		blank=False,
		verbose_name="Font Size in Points",
		help_text="Default: 11.0"
	)

	margin_left = models.FloatField(
		default=None,
		null=True,
		blank=True,
		verbose_name="Margin Left in Units",
		help_text="Default is 1cm, Set Null to use default"
	)
	
	margin_right = models.FloatField(
		default=None,
		null=True,
		blank=True,
		verbose_name="Margin Right in Units",
		help_text="Default is 1cm, Set Null to use default"
	)
	
	margin_top = models.FloatField(
		default=None,
		null=True,
		blank=True,
		verbose_name="Margin Top in Units",
		help_text="Default is 1cm, Set Null to use default"
	)
	
	def __str__(self):
				return "Print Configuration"
	class Meta:
			verbose_name = "Print Configuration"