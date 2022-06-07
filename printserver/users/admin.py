from django.contrib import admin
from .models import MyUser, TeamUser
# Register your models here.
from django.contrib.auth.forms import UserCreationForm, UserChangeForm

@admin.register(MyUser)
class MyUserAdmin(admin.ModelAdmin):
	add_form = UserCreationForm
	form = UserChangeForm
	list_display =  ('username','is_team','is_printer')
	list_filter = ('username','is_team','is_printer')
	search_fields = ('username','is_team','is_printer')

@admin.register(TeamUser)
class TeamUserAdmin(admin.ModelAdmin):
	pass
	# list_display = ('user','team_name','location')
	# list_filter = ('user','team_name','location')
	# search_fields = ('user','team_name','location')
