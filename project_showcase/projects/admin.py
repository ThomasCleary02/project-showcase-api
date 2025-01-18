from django.contrib import admin
from .models import Project

@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list__display = ('title', 'affiliation', 'created_at')
    search_fields = ('title', 'affiliation')
    list_filter = ('created_at',)