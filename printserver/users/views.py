from django.shortcuts import render,redirect
from django.contrib.auth import authenticate, login, logout
# Create your views here.

def home_view(request):
	if not request.user.is_authenticated:
		return redirect('login')
	if request.user.is_team:
		return redirect('status')
	if request.user.is_printer:
		return redirect('list')
	return redirect('status')

def login_view(request):
	if request.user.is_authenticated:
		return redirect('status')
	if request.method == 'POST':
		username = request.POST['username']
		password = request.POST['password']
		user = authenticate(request, username=username, password=password)
		if user is not None:
			login(request, user)
			return home_view(request)
		else:
			return render(request, 'login.html', {'error': 'Invalid username or password'})
	return render(request, 'login.html')


def status_view(request):
	return render(request, 'status.html')

def logout_view(request):
	logout(request)
	return redirect('login')