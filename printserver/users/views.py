from django.shortcuts import render,redirect
from django.contrib.auth import authenticate, login, logout
# Create your views here.

def login_view(request):
	if request.method == 'POST':
		username = request.POST['username']
		password = request.POST['password']
		user = authenticate(request, username=username, password=password)
		if user is not None:
			login(request, user)
			return redirect('status')
		else:
			return render(request, 'login.html', {'error': 'Invalid username or password'})
	return render(request, 'login.html')


def status_view(request):
	return render(request, 'status.html')

def logout_view(request):
	logout(request)
	return redirect('login')