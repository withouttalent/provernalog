from django.contrib import admin
from .models import Report, SourceReport
# Register your models here.


@admin.register(Report)
class ReportAdmin(admin.ModelAdmin):
    list_display = ("city", "title", "date_added")
    list_filter = ("city",)
    search_fields = ("title",)
    date_hierarchy = "date_added"


@admin.register(SourceReport)
class SourceReportAdmin(admin.ModelAdmin):
    list_display = ("region", "title", "date_relevance",)
    list_filter = ("title",)
    search_fields = ("title",)
    date_hierarchy = "date_relevance"