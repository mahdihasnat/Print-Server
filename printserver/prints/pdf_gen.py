from fpdf import FPDF
import io
from .models import Prints, PrintConfiguration
from django.utils import timezone

# path supported for Windows, Linux, and Mac
import pathlib
path_to_font = pathlib.Path(__file__).parent.absolute() / 'fonts'

FONT_NAME = 'ConsolasR'
# FONT_FILE_NAME = 'consolas/R.TTF'
# FONT_FILE_NAME = 'monoid/R.TTF'
FONT_FILE_NAME = 'hack/R.TTF'

class PDF(FPDF):

	def __init__(self, print_id:str, location, team_name, conf, *args, **kwargs):
		super(PDF, self).__init__(*args, **kwargs)
		self.print_id = print_id
		self.location = location
		self.team_name = team_name
		self.conf = conf
	
	def transform_text(self,txt:str)->str:
		return txt.replace("\t","    ").replace("{nb}","{ nb }")

	def add_cell(self,txt,ln=0):
			# self.cell(
			# 				w=len(txt)*FONT_WIDTH,
			# 				h=LINE_HEIGHT,
			# 				txt=txt,
			# 				border= 0,ln = ln,
			# 				align='L',fill=False
			# 		)
			self.write(
				h=self.conf.line_height,
				txt=txt+ ("\n" if ln == 1 else "")
			)

	def header(self):
		# Consolas regular with font_size
		self.set_font(FONT_NAME, '', self.conf.font_size)

		# PrintID
		self.add_cell("#"+self.print_id)
		self.add_cell("|Team: "+self.team_name,0)
		self.add_cell("|Location: "+ self.location,0)
		self.add_cell("|Page: "+ str(self.page_no()) + '/{nb}' ,1)
		self.dashed_line(self.get_x(),self.get_y(),self.w-self.get_x(),self.get_y())

	def init(self):
		self.add_font(FONT_NAME, '',path_to_font / FONT_FILE_NAME, uni=True)
		self.set_auto_page_break(True)	
		self.alias_nb_pages()
		if self.conf.margin_left is not None :
			self.set_left_margin(self.conf.margin_left)
		if self.conf.margin_right is not None :
			self.set_right_margin(self.conf.margin_right)
		if self.conf.margin_top is not None :
			self.set_top_margin(self.conf.margin_top)
		self.add_page()
	
	def add_source_code(self,source_code):
		# self.set_font(FONT_NAME, '', self.conf.font_size)
		self.write(self.conf.line_height,self.transform_text(source_code))
	
def get_pdf(print):
	# Instantiation of inherited class
	conf = PrintConfiguration.get_solo()
	pdf = PDF(
			print_id=str(print.print_id),
			location=str(print.owner.location),
			team_name=str(print.owner.get_name()),
			conf=conf,
			orientation=conf.orientation, unit=conf.unit, format=conf.paper_type
			)

	pdf.init()
	pdf.add_source_code(print.source_code)

	print.status = Prints.Status.PRINTING
	print.printing_time = timezone.now()
	print.total_page = pdf.page_no()
	print.save()

	buffer = io.BytesIO(pdf.output(dest='S').encode('latin-1'))
	return buffer

def set_pagecount(print):
	conf = PrintConfiguration.get_solo()
	pdf = PDF(
			print_id=str(print.print_id),
			location=str(print.owner.location),
			team_name=str(print.owner.get_name()),
			conf=conf,
			orientation=conf.orientation, unit=conf.unit, format=conf.paper_type
			)

	pdf.init()
	pdf.add_source_code(print.source_code)
	print.total_page = pdf.page_no()
	return 

def save_pdf(print, file_path):
	# Instantiation of inherited class
	conf = PrintConfiguration.get_solo()
	pdf = PDF(
			print_id=str(print.print_id),
			location=str(print.owner.location),
			team_name=str(print.owner.get_name()),
			conf=conf,
			orientation=conf.orientation, unit=conf.unit, format=conf.paper_type
			)

	pdf.init()
	pdf.add_source_code(print.source_code)
	pdf.output(file_path,dest='F')
	return