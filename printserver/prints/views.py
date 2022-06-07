from django.http import FileResponse
from django.shortcuts import redirect, render

from .models import Prints
from .pdf_gen import get_pdf

from users.models import TeamUser

def list_view(request):
	if not request.user.is_authenticated or not request.user.is_printer:
		return redirect('login')
	return render(request, 'list.html',{'prints':Prints.objects.all()})

def pdf_view(request,print_id):
	print_id = str(print_id)
	if not request.user.is_authenticated or not request.user.is_printer:
		return redirect('login')
	try:
		
		prints = Prints.objects.get(print_id=print_id)
		return FileResponse(get_pdf(prints), as_attachment=False, filename=print_id+'.pdf')
	except Prints.DoesNotExist:
		return redirect('list')

def submit_view(request):
	if not request.user.is_authenticated or not request.user.is_team:
		return redirect('home')
	if request.method == 'POST':
		tag = request.POST['tag']
		source_code = request.POST['source_code']
		team_user = TeamUser.objects.get(user=request.user)
		prints = Prints(owner=team_user, tag=tag, source_code=source_code)
		prints.save()
		return redirect('status')
	return render(request, 'submit.html')
