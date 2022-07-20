from webbrowser import get
from users.models import MyUser, TeamUser, PrinterUser, Lab
from django.contrib.auth.models import Group , Permission
from django.db.utils import IntegrityError
import csv
import time
import random

PRINTER_GROUP_NAME = 'printer'

def create_printer_group():
	try:
		group = Group.objects.get(name=PRINTER_GROUP_NAME)
	except Group.DoesNotExist:
		print("Group does not exist")
		group = Group.objects.create(name=PRINTER_GROUP_NAME)
		group.save()
	
	group.permissions.add(Permission.objects.get(name='Can add prints'))
	group.permissions.add(Permission.objects.get(name='Can change prints'))
	group.permissions.add(Permission.objects.get(name='Can delete prints'))
	group.permissions.add(Permission.objects.get(name='Can view prints'))
	
	group.permissions.add(Permission.objects.get(name='Can add Print Configuration'))
	group.permissions.add(Permission.objects.get(name='Can change Print Configuration'))
	group.permissions.add(Permission.objects.get(name='Can delete Print Configuration'))
	group.permissions.add(Permission.objects.get(name='Can view Print Configuration'))
	group.save()

def get_lab(lab_name):
	try:
		lab = Lab.objects.get(name=lab_name.upper())
		return lab
	except Lab.DoesNotExist:
		lab = Lab.objects.create(name=lab_name.upper())
		lab.save()
		return lab

PL = get_lab("PL")
DBL = get_lab("DBL")
WNL = get_lab("WNL")
VLSI = get_lab("VLSI")
BIO = get_lab("BIO")
CL = get_lab("CL")
IAC = get_lab("IAC")


def add_groups(user,groupname):
	try:
		group = Group.objects.get(name=groupname)
		group.user_set.add(user)
		group.save()
	except Group.DoesNotExist:
		print("Group does not exist")
		create_printer_group()
		print("Group created")
		return add_groups(user,groupname)
		# Add can view prints to group

def add_team(username, password, team_name, lab_name, location):
	try:
		user = MyUser.objects.get(username=username)
	except MyUser.DoesNotExist:
		user = MyUser.objects.create_user(username=username, password=password,name=team_name)
	user.name = team_name
	user.set_password(password)
	user.is_team = True
	user.is_printer = False
	user.save()
	try:
		team = TeamUser.objects.get(user=user)
	except TeamUser.DoesNotExist:
		team = TeamUser.objects.create(user=user, location=location)
	
	team.lab = get_lab(lab_name)
	team.location = location
	team.save()

def add_printer(username, password):
	try:
		user = MyUser.objects.get(username=username)
	except MyUser.DoesNotExist:
		user = MyUser.objects.create_user(username=username, password=password)
	user.set_password(password)
	user.is_team = False
	user.is_printer = True
	user.is_staff = True
	user.save()
	try:
		printer = PrinterUser.objects.get(user=user)
	except PrinterUser.DoesNotExist:
		printer = PrinterUser.objects.create(user=user)
	add_groups(user, PRINTER_GROUP_NAME)
	printer.save()

def add_superuser(username, password):
	try:
		user = MyUser.objects.get(username=username)
	except MyUser.DoesNotExist:
		user = MyUser.objects.create_superuser(username=username, password=password)
	user.set_password(password)
	user.save()


def add_locust_data():
	users = []
	TOTAL_USER = 120
	for i in range(TOTAL_USER):
		username = 'lt' + str(i)
		password = 'lt' + str(i)
		team_name = 'lt' + str(i)
		user = MyUser()
		user.username = username
		user.name = "lucast team "+str(i)
		user.set_password(password)
		user.is_team = True
		user.is_printer = False
		users.append(user)
	try:
		MyUser.objects.bulk_create(users)
	except IntegrityError as ie:
		MyUser.objects.bulk_update(users, ['name', 'password', 'is_team', 'is_printer'])
	
	for i in range(TOTAL_USER):
		team_user = TeamUser()
		team_user.lab = random.choice([PL, DBL, WNL, VLSI, BIO, CL, IAC])
		team_user.location = '1-1'
		team_user.user = users[i]
		users[i]=team_user

	try:
		TeamUser.objects.bulk_create(users)
	except IntegrityError as ie:
		TeamUser.objects.bulk_update(users, ['lab', 'location'])
	
def add_from_csv(csv_file_name):
	# format: row_number , Team_name , Location , Username, Password
	with open(csv_file_name, 'r') as file:
		reader = csv.reader(file)
		for row in reader:
			username = row[3]
			password = row[4]
			team_name = row[1]
			location = row[2]
			lab_name = "Lab"
			add_team(username, password, team_name, lab_name, location)


# create_printer_group()
start_time = time.time()
add_superuser('admin', 'admin')
add_team("t1","t1","Team one","DBL","1-2")
add_team("t2","t2","Team two","BIO","2-3")
add_printer("p1","p1")
add_locust_data()
end_time = time.time()
print("All data added")
print("Time taken: ", end_time - start_time)