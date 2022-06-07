from django.shortcuts import redirect, render

from .models import Prints


def list_view(request):
	if not request.user.is_authenticated or not request.user.is_printer:
		return redirect('login')
	return render(request, 'list.html',{'prints':Prints.objects.all()})