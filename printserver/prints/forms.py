from pyexpat import model
from django import forms
from django.forms import ModelForm
from prints.models import Prints


class SubmitForm(ModelForm):
	class Meta:
		model = Prints
		fields = ['source_code']
		widgets = {
			'source_code': forms.Textarea(attrs={'class': 'form-control'})
		}