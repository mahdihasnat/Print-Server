from .models import Prints
from .pdf_gen import get_pdf, save_pdf
from django.conf import settings


def save_to_file(prints):
	# returns path to file
	file_name = str(prints.print_id) + '.pdf'
	# print( "file root: ", settings.PRINT_FILES_DIR)
	file_path = settings.PRINT_FILES_DIR / file_name
	save_pdf(prints, file_path)
	print("file saved to: ", file_path)
	return file_path

def do_prints(prints):
	file_path = save_to_file(prints)
	# print( "file path: " , file_path)
	


def add_prints(prints):
	do_prints(prints)