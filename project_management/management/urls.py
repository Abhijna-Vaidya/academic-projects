# urls.py

from django.urls import path
from .views import change_password, forgotPassword, guide_forgotPassword, notifications, notify, save_subscription,  upload_csv, create_group, upload_project, search_members,student_login,student_dashboard,student_logout, view_doc,guide_login, guide_dashboard, view_groups
from .views import student_autocomplete, domain_autocomplete, upload_evaluation, download_reference_csv_f, download_reference_csv_s

urlpatterns = [
    path('upload-csv/', upload_csv, name='upload_csv'),
    path('download-reference-faculty/', download_reference_csv_f, name='download_reference_f'),
    path('download-reference-student/', download_reference_csv_s, name='download_reference_s'),
    path('create-group/', create_group, name='create_group'),
    path('upload_project/', upload_project, name='upload_project'),
    path('search-members/', search_members, name='search_members'),
    path('login/', student_login, name='student_login'),
    path('dashboard/', student_dashboard, name='student_dashboard'),
    path('uploded_documents/', view_doc, name='view_doc'),
    path('logout/', student_logout, name='student_logout'),
    path('guide/login/', guide_login, name='guide_login'),
    path('guide/dashboard/', guide_dashboard, name='guide_dashboard'),
    path('forgotPassword/', forgotPassword, name='forgotPassword'),
    path('guide/forgotPassword/', guide_forgotPassword, name='guide_forgotPassword'),
    path('change_password/', change_password, name='change_password'),
    path('student-autocomplete/', student_autocomplete, name='student-autocomplete'),
    path('domain-autocomplete/', domain_autocomplete, name='domain-autocomplete'),
    path('upload_evaluation/<int:group_id>/', upload_evaluation, name='upload_evaluation'),
    path('notifications/', notifications, name='notifications'),
    path('save-subscription/', save_subscription, name='save_subscription'),
    path('guide/notify/', notify, name='notify'),
    
]

