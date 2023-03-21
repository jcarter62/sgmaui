from django.contrib import admin
from . import models
from import_export.admin import ImportExportModelAdmin


class SessionDataAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    list_display = ['session', 'key_name', 'key_text', 'created', 'updated']
    list_editable = ['key_name', 'key_text']
    search_fields = ['session', 'key_name']
    list_per_page = 10
    save_as = True


admin.site.register(models.SessionData, SessionDataAdmin)

