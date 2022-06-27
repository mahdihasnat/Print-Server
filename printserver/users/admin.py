from django.contrib import admin
from .models import MyUser, TeamUser, PrinterUser
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth import get_user_model
class MyUserCreationForm(UserCreationForm):
	class Meta:
		model = get_user_model()
		fields = ('username',)

@admin.register(MyUser)
class MyUserAdmin(admin.ModelAdmin):
	form = UserChangeForm
	list_display =  ('username','is_team','is_printer')
	list_filter = ('username','is_team','is_printer')
	search_fields = ('username','is_team','is_printer')

	def get_form(self, request, obj=None, **kwargs):
		if obj is None:
			return MyUserCreationForm
		else:
			return UserChangeForm

@admin.register(TeamUser)
class TeamUserAdmin(admin.ModelAdmin):
	
	list_display = ('user','location')
	list_filter = ('user','location')
	search_fields = ('user','location')

@admin.register(PrinterUser)
class PrinterUserAdmin(admin.ModelAdmin):
	list_display = ('user',)
	list_filter = ('user',)
	search_fields = ('user',)