from users.models import MyUser, TeamUser, PrinterUser
# Import DoesnotExist exception from django.db.models.base


def add_team(username, password, team_name, location):
	try:
		user = MyUser.objects.get(username=username)
	except MyUser.DoesNotExist:
		user = MyUser.objects.create_user(username=username, password=password)
	user.set_password(password)
	user.is_team = True
	user.is_printer = False
	user.save()
	try:
		team = TeamUser.objects.get(user=user)
	except TeamUser.DoesNotExist:
		team = TeamUser.objects.create(user=user, team_name=team_name, location=location)
	team.team_name = team_name
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
	user.save()
	try:
		printer = PrinterUser.objects.get(user=user)
	except PrinterUser.DoesNotExist:
		printer = PrinterUser.objects.create(user=user)
	printer.save()

def add_superuser(username, password):
	try:
		user = MyUser.objects.get(username=username)
	except MyUser.DoesNotExist:
		user = MyUser.objects.create_superuser(username=username, password=password)
	print("user: ", user)
	user.set_password(password)
	user.save()

add_superuser('admin', 'admin')
add_team("t1","t1","Team one","DBL")
add_printer("p1","p1")
