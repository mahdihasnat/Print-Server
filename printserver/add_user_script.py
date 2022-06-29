from users.models import MyUser, TeamUser, PrinterUser
from django.contrib.auth.models import Group , Permission
import csv

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


def add_groups(user,groupname):
	try:
		group = Group.objects.get(name=groupname)
	except Group.DoesNotExist:
		assert(False)

		# Add can view prints to group
	group.user_set.add(user)
	group.save()

def add_team(username, password, team_name, location):
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


def add_from_csv(csv_file_name):
	# format: row_number , Team_name , Location , Username, Password
	with open(csv_file_name, 'r') as file:
		reader = csv.reader(file)
		for row in reader:
			username = row[3]
			password = row[4]
			team_name = row[1]
			location = row[2]
			add_team(username, password, team_name, location)


# create_printer_group()
# add_superuser('admin', 'admin')
# add_team("t1","t1","Team one","DBL")
# add_team("t2","t2","Team two","BIO")
# add_printer("p1","p1")

# print("All data added")

add_from_csv("")