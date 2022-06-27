from django.http import FileResponse
from django.shortcuts import redirect, render

from .models import Prints
from .pdf_gen import get_pdf
from .forms import SubmitForm

from users.models import TeamUser

def pdf_view(request,print_id):
	print_id = str(print_id)
	if not request.user.is_authenticated or request.user.is_team:
		return redirect('login')
	try:
		prints = Prints.objects.get(print_id=print_id)
		prints.status = Prints.Status.PRINTING
		prints.save()	
		return FileResponse(get_pdf(prints), as_attachment=False, filename=print_id+'.pdf')
	except Prints.DoesNotExist:
		return redirect('home')

def submit_view(request):
	if not request.user.is_authenticated or not request.user.is_team:
		return redirect('home')


	if request.method == 'POST':
		form = SubmitForm(request.POST)
		if form.is_valid():				
			team_user = TeamUser.objects.get(user=request.user)
			prints = Prints(owner=team_user , **form.cleaned_data)
			prints.save()
			return redirect('status')
	
	return render(request, 'submit.html',{'form':SubmitForm(initial={'owner':request.user})})
