from django.http import FileResponse
from django.shortcuts import redirect, render

from .models import Prints
from .pdf_gen import get_pdf

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