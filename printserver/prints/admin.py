from django.contrib import admin
from .models import Prints
from django.utils.html import format_html

@admin.action(description="Mark Selected prints as printed")
def make_printed(modeladmin, request, queryset):
	queryset.update(status=Prints.Status.PRINTED)


@admin.register(Prints)
class PrintsAdmin(admin.ModelAdmin):
	list_display = ('print_id', 'owner', 'tag', 'submission_time', 'view_pdf', 'total_page', 'status')
	list_display_links = ('view_pdf',)
	list_editable = ('status',)
	list_filter = ('owner', 'status','submission_time', 'total_page')
	search_fields = ('print_id', 'owner', 'tag', 'source_code', 'submission_time', 'printing_time', 'total_page', 'status')
	ordering = ('submission_time',)
	actions = [make_printed]

	def view_pdf(self,obj):
		return format_html('<a href="/pdf/{0}.pdf">View Pdf</a>', obj.print_id)
