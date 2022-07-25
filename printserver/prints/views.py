from django.conf import settings
from django.http import FileResponse
from django.shortcuts import redirect, render
from django.contrib import messages


from .models import Prints
from .pdf_gen import get_pdf, set_pagecount
from .forms import SubmitForm
from .printer import add_prints

from users.models import TeamUser


def pdf_view(request,print_id):
	print_id = str(print_id)
	if not request.user.is_authenticated or request.user.is_team:
		return redirect('login')
	try:
		prints = Prints.objects.get(print_id=print_id)
		return FileResponse(get_pdf(prints), as_attachment=False, filename=print_id+'.pdf')
	except Prints.DoesNotExist:
		return redirect('home')


def submit_view(request):
	if not request.user.is_authenticated or not request.user.is_team:
		return redirect('home')
	
	team_user = TeamUser.objects.get(user=request.user)

	if request.method == 'POST':
		form = SubmitForm(request.POST)
		if form.is_valid():				
			prints = Prints(owner=team_user, **form.cleaned_data)
			set_pagecount(prints)
			if team_user.get_total_page_usage() + prints.total_page <= settings.MAX_PAGE_COUNT:
				prints.save()
				messages.success(request,'Print request submitted successfully')
				try:
					add_prints(prints)
				except:
					print("Auto Print Failed: print id: ", prints.print_id)
				
				return redirect('status')
			else:
				messages.error(request, 'Request Failed! Page limit exceedded')
				return redirect('home')
	messages.warning(request,"Remaining pages: "+str(settings.MAX_PAGE_COUNT - team_user.get_total_page_usage()))
	return render(request, 'submit.html', {'form': SubmitForm(initial={'owner': request.user})})
