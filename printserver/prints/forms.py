from pyexpat import model
from django.forms import ModelForm
from prints.models import Prints

class SubmitForm(ModelForm):
	class Meta:
		model = Prints
		fields = ['source_code']