from django.contrib import admin
from .models import Prints

@admin.register(Prints)
class PrintsAdmin(admin.ModelAdmin):
	list_display = ('print_id', 'owner', 'tag', 'submission_time', 'printing_time', 'total_page', 'status')
	list_filter = ('owner', 'status','submission_time', 'total_page')
	search_fields = ('print_id', 'owner', 'tag', 'source_code', 'submission_time', 'printing_time', 'total_page', 'status')
	ordering = ('-submission_time',)
