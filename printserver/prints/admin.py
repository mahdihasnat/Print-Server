from django.contrib import admin
from .models import Prints
from django.utils.html import format_html
from .filters import LabFilter

@admin.action(description="Mark Selected prints as Delivered")
def make_delivered(modeladmin, request, queryset):
	queryset.update(status=Prints.Status.DELIVERED)


@admin.register(Prints)
class PrintsAdmin(admin.ModelAdmin):
	list_display = ('print_id', 'owner', 'submission_time', 'view_pdf', 'total_page', 'status')
	list_display_links = ('print_id','view_pdf',)
	list_editable = ('status',)
	list_filter = ('status','submission_time', 'total_page',LabFilter)
	search_fields = ['print_id', 'owner__user__name','owner__user__username', 'source_code', 'submission_time', 'printing_time', 'total_page', 'status']
	ordering = ('-submission_time',)
	actions = [make_delivered]
	list_per_page = 10

	def view_pdf(self,obj):
		return format_html('<a href="/pdf/{0}.pdf">View Pdf</a>', obj.print_id)
	class Media:
		js = ['js/auto_refresher.js']

from solo.admin import SingletonModelAdmin
from .models import PrintConfiguration

admin.site.register(PrintConfiguration, SingletonModelAdmin)
