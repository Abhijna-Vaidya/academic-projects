import csv
from .models import  Update, Attachment
from pyexpat.errors import messages
from django.contrib import admin
from .models import Student, Faculty, Domain, Group
from .forms import  GroupAdminForm
from django.utils.html import format_html
from django.contrib import admin
from .models import Student, Group, Domain
from django.utils.translation import gettext_lazy as _
from django.http import HttpResponse
import zipfile
import os
from django.conf import settings
from django.utils.timezone import now

admin.site.site_header="Project Manager"
admin.site.site_title="Project Manager Portal"
admin.site.index_title=" "

class NotInGroupFilter(admin.SimpleListFilter):
    title = _('Students Not in Any Group')  # The label for the filter
    parameter_name = 'not_in_group'  # The name of the filter parameter in the URL query

    def lookups(self, request, model_admin):
        return (
            ('Yes', _('Not in Any Group')),
        )

    def queryset(self, request, queryset):
        if self.value() == 'Yes':
            return queryset.filter(members__isnull=True)  # Filter students who are not in any group
        return queryset
    
# Customizing the Student admin page
class StudentAdmin(admin.ModelAdmin):
    list_display = ('name', 'usn', 'section', 'get_groups')  # Columns to display in the list view
    search_fields = ('name', 'usn')  # Add a search box for name and USN
    list_filter = ('section', NotInGroupFilter)  # Add filters for section and year
    ordering = ('usn',)  # Default ordering of students by USN

    def get_groups(self, obj):
        return ", ".join([group.batch_number for group in obj.members.all()]) if obj.members.exists() else "No Groups"

    get_groups.short_description = "Groups"


class FacultyAdmin(admin.ModelAdmin):
    list_display = ('name', 'designation', 'experience', 'domain')  # Columns to display in the list view
    search_fields = ('name', 'domain')  # Add a search box for name and USN
    list_filter = ('name',)  # Add filters for section and year
    ordering = ('name',)  

class ReviewDoneFilter(admin.SimpleListFilter):
    title = _('Review Status')  # The label for the filter in the sidebar
    parameter_name = 'review_done'  # The name of the parameter in the URL query

    def lookups(self, request, model_admin):
        return (
            ('Yes', _('Review Done')),
            ('No', _('Review Pending')),
        )

    def queryset(self, request, queryset):
        if self.value() == 'Yes':
            return queryset.filter(review_done=True)
        elif self.value() == 'No':
            return queryset.filter(review_done=False)
        return queryset
    
class ReportUploadedFilter(admin.SimpleListFilter):
    title = _('Report Uploaded')  # The label for the filter in the sidebar
    parameter_name = 'report_uploaded'  # The name of the parameter in the URL query

    def lookups(self, request, model_admin):
        return (
            ('Yes', _('Report Uploaded')),
            ('No', _('Report Not Uploaded')),
        )

    def queryset(self, request, queryset):
        if self.value() == 'Yes':
            return queryset.filter(project_report__isnull=False)
        elif self.value() == 'No':
            return queryset.filter(project_report__isnull=True)
        return queryset


# Custom Filter for PPT Uploaded
class PPTUploadedFilter(admin.SimpleListFilter):
    title = _('PPT Uploaded')  # The label for the filter in the sidebar
    parameter_name = 'ppt_uploaded'  # The name of the parameter in the URL query

    def lookups(self, request, model_admin):
        return (
            ('Yes', _('PPT Uploaded')),
            ('No', _('PPT Not Uploaded')),
        )

    def queryset(self, request, queryset):
        if self.value() == 'Yes':
            return queryset.filter(project_ppt__isnull=False)
        elif self.value() == 'No':
            return queryset.filter(project_ppt__isnull=True)
        return queryset
    
# Customizing the Group admin page
class GroupAdmin(admin.ModelAdmin):
    list_display = ('batch_number', 'get_leader_with_usn', 'domain', 'get_members', 'get_guide')  # Display the leader and domain
    search_fields = ('batch_number','leader__name', 'domain__name','members__usn')  # Add search functionality for leader name and domain
    list_filter = ('domain', ReviewDoneFilter, ReportUploadedFilter, PPTUploadedFilter)  # Add filters for domain
    fields = ['batch_number','leader', 'get_members','domain', 'guide', 'project_report','review_done','members']
    readonly_fields = ['get_members']
    actions = ['zip_uploads']
    form = GroupAdminForm
    
    class Media:
        css = {
            'all': ('admin/css/custom_select2.css',)
        }

    # Method to display members in list view
    def get_leader_with_usn(self, obj):
        return f"{obj.leader.name} ({obj.leader.usn})" if obj.leader else "No Leader Assigned"
    
    # Method to display members with their USNs in the list view
    def get_members(self, obj):
        return format_html("<br>".join([f"{member.name} ({member.usn})" for member in obj.members.all()]))
    
    def get_guide(self,obj):
        guide_name = obj.guide.name if obj.guide else "Not Assigned"
        return guide_name
    
    def zip_uploads(self, request, queryset):
        # Specify the folder where your uploads are stored
        folder_path = os.path.join(settings.MEDIA_ROOT, 'uploads/final_reports')
        zip_filename = f"uploads_{now().strftime('%Y')}.zip"
        
        # Create a zip file
        zip_file_path = os.path.join(settings.MEDIA_ROOT, zip_filename)
        
        with zipfile.ZipFile(zip_file_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
            # Walk through the directory and add files to the zip
            for root, dirs, files in os.walk(folder_path):
                for file in files:
                    file_path = os.path.join(root, file)
                    zipf.write(file_path, os.path.relpath(file_path, folder_path))  # Preserve the directory structure
        
        # Return the zip file for download
        with open(zip_file_path, 'rb') as f:
            response = HttpResponse(f.read(), content_type='application/zip')
            response['Content-Disposition'] = f'attachment; filename="{zip_filename}"'
            return response
    
    zip_uploads.short_description = 'Download All Uploaded Files as ZIP'
    
    get_members.short_description = "Group Members"
    get_guide.short_description = "Group Guide"
    get_leader_with_usn.short_description = "Group Leader"


class AttachmentInline(admin.TabularInline):
    model = Attachment
    extra = 1  # Number of empty forms to display

class UpdateAdmin(admin.ModelAdmin):
    inlines = [AttachmentInline]

# Register models with their custom admin classes
admin.site.register(Student, StudentAdmin)
admin.site.register(Group, GroupAdmin)
admin.site.register(Domain)
admin.site.register(Faculty, FacultyAdmin)
admin.site.register(Update, UpdateAdmin)

