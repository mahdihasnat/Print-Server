from users.models import MyUser, TeamUser, PrinterUser
from django.contrib.auth.models import Group , Permission

PRINTER_GROUP_NAME = 'printer'

def create_printer_group():
	try:
		group = Group.objects.get(name=PRINTER_GROUP_NAME)
	except Group.DoesNotExist:
		group = Group.objects.create(name=PRINTER_GROUP_NAME)
	
	group.permissions.add(Permission.objects.get(name='Can add prints'))
	group.permissions.add(Permission.objects.get(name='Can change prints'))
	group.permissions.add(Permission.objects.get(name='Can delete prints'))
	group.permissions.add(Permission.objects.get(name='Can view prints'))
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

create_printer_group()
add_superuser('admin', 'admin')
add_team("t1","t1","Team one","DBL")
add_printer("p1","p1")

print("All data added")