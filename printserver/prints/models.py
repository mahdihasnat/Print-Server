from django.db import models
from solo.models import SingletonModel

class Prints(models.Model):

	class Status(models.IntegerChoices):
		SENT = 1
		QUEUED = 2
		PRINTING = 3
		PRINTED = 4
		DELIVERING = 5
		DELIVERED = 6

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


	def __str__(self):
				return "Print Configuration"
	class Meta:
			verbose_name = "Print Configuration"