from django.contrib import admin
from async_parser.models import TaskFile, ParserTask


@admin.register(ParserTask)
class ParserTaskAdminDisplay(admin.ModelAdmin):

    class TaskFileAdminInline(admin.TabularInline):
        model = TaskFile
        extra = 0

        def has_add_permission(self, request, obj):
            return False

        def has_change_permission(self, request, obj=None):
            return False

    list_display = ('path', 'city', 'group_type', 'date_created', 'date_relevance')
    search_fields = ('path',)
    list_filter = ('group_type',)
    date_hierarchy = 'date_created'
    inlines = [TaskFileAdminInline, ]


@admin.register(TaskFile)
class TaskFileAdminDisplay(admin.ModelAdmin):
    list_display = ('path', 'is_parsed', 'celery_id', 'progress_parsing', 'date_parsed')
    search_fields = ('path',)
    list_filter = ('is_parsed',)

    def progress_parsing(self, obj):
        if obj.parsed_parcels and obj.parcels:
            return f'{obj.parsed_parcels}/{obj.parcels}'
        else:
            return "0/0"





