from django.contrib import admin
from .models import MyUser, TeamUser
# Register your models here.

@admin.register(MyUser)
class MyUserAdmin(admin.ModelAdmin):
	list_display =  ('username','is_team','is_printer')
	list_filter = ('userame','is_team','is_printer')
	search_fields = ('username','is_team','is_printer')

@admin.register(TeamUser)
class UserAdmin(admin.ModelAdmin):
	list_display = ('username','team_name','location')
	list_filter = ('team_name','location')
	search_fields = ('username','team_name','location')
	ordering = ('username',)
