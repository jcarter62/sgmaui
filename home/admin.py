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

class Sys_SettingsAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    list_display = ['setting_name', 'setting_text']
    list_editable = ['setting_text']
    search_fields = ['setting_name']
    list_per_page = 10
    save_as = True


admin.site.register(models.SystemInfo, Sys_SettingsAdmin)
