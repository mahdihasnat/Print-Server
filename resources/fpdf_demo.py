import fpdf
from fpdf import FPDF

import pathlib
# path supported for Windows, Linux, and Mac
path_to_font = pathlib.Path(__file__).parent.absolute() / 'fonts'


FONT_NAME = 'ConsolasR'
TEAM_NAME = 'BUET HELLO WORLD'

class PDF(FPDF):

    def __init__(self, print_id:str, location, team_name, *args, **kwargs):
        super(PDF, self).__init__(*args, **kwargs)
        self.print_id = print_id
        self.location = location
        self.team_name = team_name
        


    def header(self):
        # Consolas regular 15
        self.set_font(FONT_NAME, '', 15)


        # PrintID
        self.cell(0,10, '# '+self.print_id,0,1,'L')
        self.cell(0,10, 'Team:'+self.team_name,0,1,'L')
        # Title
        self.cell(30, 10, 'Title', 1, 0, 'C')
        # Line break
        self.ln(20)

    # Page footer
    def footer(self):
        # Position at 1.5 cm from bottom
        self.set_y(-15)
        # Arial italic 8
        self.set_font('Arial', 'I', 8)
        # Page number
        self.cell(0, 10, 'Page ' + str(self.page_no()) + '/{nb}', 0, 0, 'C')



# Instantiation of inherited class
pdf = PDF(
    print_id='1',
    location='WNL Row 1 Col 3',
    team_name="BUET HELLO WORLD",
    orientation='P', unit='mm', format='A4'
    )

pdf.add_font(FONT_NAME, '',path_to_font / 'CONSOLA.TTF', uni=True)
pdf.set_auto_page_break(True)

pdf.alias_nb_pages()
pdf.add_page()

pdf.set_font('ConsolasR', '', 12)
for i in range(1, 41):
    pdf.cell(0, 10, 'Printing line number ' + str(i), 0, 1)
pdf.cell(0,10,'!@#$%^&*')
pdf.output('tuto2.pdf', 'F')

