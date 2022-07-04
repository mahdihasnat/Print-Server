from users.models import Lab
from django.utils.translation import gettext_lazy as _
from django_admin_multiple_choice_list_filter.list_filters import MultipleChoiceListFilter

class LabFilter(MultipleChoiceListFilter):

	title = _("Lab")
	parameter_name = 'owner__lab__id'

	def lookups(self, request, model_admin):
		"""
        Returns a list of tuples. The first element in each
        tuple is the coded value for the option that will
        appear in the URL query. The second element is the
        human-readable name for the option that will appear
        in the right sidebar.
        """
		
		return [ (lab.id, lab.name) for lab in Lab.objects.all()]
	