from tracemalloc import start
from django.test import TestCase
from django.utils import timezone
from .models import MyUser,TeamUser,Lab
import random

TOTAL_TEAM = 130
class TeamUserTestCase(TestCase):

	def get_lab(self,lab_name):
		try:
			lab = Lab.objects.get(name=lab_name)
		except Lab.DoesNotExist:
			lab = Lab.objects.create(name=lab_name)
		return lab

	def setUp(self):
		start_time = timezone.now()
		teams = []
		for i in range(TOTAL_TEAM):
			username = 't' + str(i)
			password = 't' + str(i)
			user = MyUser()
			team_name = 't'*25
			user.username = username
			user.password = password
			user.name = team_name
			teams.append(user)
		MyUser.objects.bulk_create(teams)

		for i in range(TOTAL_TEAM):
			lab = self.get_lab( random.choice(['PL','DBL','WNL','IAC','CL','VDAL','BIO']))
			teams[i]=TeamUser(user= teams[i], lab= lab, location= 'Somewhere')
		TeamUser.objects.bulk_create(teams)

		end_time = timezone.now()
		print('Time to create '+str(TOTAL_TEAM)+' teams: ' + str(end_time - start_time))
	
	def test_lookup(self):
		start_time = timezone.now()

		for i in range(TOTAL_TEAM):
			username = 't'+ str(i)
			assert( MyUser.objects.get(username=username)!= None)
			user = MyUser.objects.get(username=username)
			team_user = TeamUser.objects.get(user=user)
			assert(team_user != None)
		
		end_time = timezone.now()
		print('Time to lookup '+str(TOTAL_TEAM)+' teams: ' + str(end_time - start_time))
	