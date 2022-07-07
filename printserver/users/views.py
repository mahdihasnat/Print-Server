from django.shortcuts import render,redirect
from django.contrib.auth import authenticate, login, logout
# Create your views here.

from prints.models import Prints
from .models import TeamUser


def home_view(request):
	if not request.user.is_authenticated:
		return redirect('login')
	if request.user.is_team:
		return redirect('submit')
	if request.user.is_staff:
		return redirect('/admin/')
	return redirect('logout')


def status_view(request):
	if not request.user.is_authenticated or not request.user.is_team:
		return redirect('home')
	team_user = TeamUser.objects.get(user=request.user)
	return render(request, 'status.html',{'prints':Prints.objects.filter(owner=team_user)})
