from django.db import models

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
	tag = models.CharField(max_length=100)
	source_code = models.TextField()

	submission_time = models.DateTimeField(auto_now_add=True)
	printing_time = models.DateTimeField(null=True)

	total_page = models.IntegerField(null=True)
	status = models.IntegerField(choices=Status.choices, default=Status.QUEUED)