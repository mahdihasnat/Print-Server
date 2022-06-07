from django.contrib import admin
from .models import TeamUser
# Register your models here.
@admin.register(TeamUser)
class UserAdmin(admin.ModelAdmin):
	list_display = ('username','team_name','location')
	list_filter = ('team_name','location')
	search_fields = ('username','team_name','location')
	ordering = ('username',)
