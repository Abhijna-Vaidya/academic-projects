# views.py
from django.http import FileResponse
import os
import csv
import json
import mimetypes
from django.conf import settings
from django.db import DatabaseError
from django.shortcuts import render, redirect, get_object_or_404
from pywebpush import webpush, WebPushException
from .forms import GroupCreationForm, ProjectFileForm, EvaluationSheetForm
from .models import Attachment, GuideAttachments, GuideNotification, PushSubscription, Student, Faculty, Group, Update
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.messages import get_messages
from .forms import StudentLoginForm,FacultyLoginForm
from .models import Student, Domain

def download_reference_csv_f(request):
    file_path = os.path.join('static', 'files', 'Faculty-Reference.csv')
    response = FileResponse(open(file_path, 'rb'), as_attachment=True, filename='Faculty-Reference.csv')
    return response
def download_reference_csv_s(request):
    file_path = os.path.join('static', 'files', 'Student-Reference.csv')
    response = FileResponse(open(file_path, 'rb'), as_attachment=True, filename='Student-Reference.csv')
    return response

@csrf_exempt
def save_subscription(request):
    if request.method == "POST":
        try:
            # Parse the subscription data from the request body
            data = json.loads(request.body)
            print(data)

            # Extract necessary fields
            usn = request.session.get('student_usn')
            endpoint = data.get("endpoint")
            keys = data.get("keys", {})
            p256dh = keys.get("p256dh")
            auth = keys.get("auth")
            if not endpoint or not p256dh or not auth:
                return JsonResponse({"error": "Invalid subscription data"}, status=400)

            # Save to the database
            try:
                subscription, created = PushSubscription.objects.update_or_create(
        usn=usn,  # Field to match on
        defaults={
            'endpoint': endpoint,
            'keys_p256dh': p256dh,
            'keys_auth': auth
        }
    )

                if not created:
                    # Update existing subscription
                    subscription.keys_p256dh = p256dh
                    subscription.keys_auth = auth
                    subscription.save()

                return JsonResponse({"success": True, "message": "Subscription saved!"})
            except DatabaseError as db_error:
                return JsonResponse({"error": f"Database error: {db_error}"}, status=500)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)
    else:
        return JsonResponse({"error": "Invalid request method"}, status=405)

def upload_evaluation(request, group_id):
    group = get_object_or_404(Group, id=group_id)

    # Check if the logged-in user is the guide for this group
    if request.session.get('faculty_name') != group.guide.name:
        messages.error(request, "You are not authorized to upload the evaluation sheet for this group.")
        return redirect('guide_dashboard')

    if request.method == 'POST':
        form = EvaluationSheetForm(request.POST, request.FILES)
        if form.is_valid():
            # Save the uploaded evaluation sheet
            evaluation_sheet = form.save(commit=False)
            evaluation_sheet.group = group
            evaluation_sheet.save()

            # Update the report status to 'True' (Approved)
            group.review_done = True
            group.save()

            messages.success(request, f"Evaluation sheet uploaded successfully for batch {group.batch_number}.")
            return redirect('guide_dashboard')
    else:
        form = EvaluationSheetForm()

    return render(request, 'upload_evaluation.html', {'form': form, 'group': group})

def student_autocomplete(request):
    if 'q' in request.GET:
        query = request.GET['q']
        students = Student.objects.filter(name__icontains=query).values('id', 'name')
        return JsonResponse({'results': list(students)})
    return JsonResponse({'results': []})

def domain_autocomplete(request):
    if 'q' in request.GET:
        query = request.GET['q']
        domains = Domain.objects.filter(name__icontains=query).values('id', 'name')
        return JsonResponse({'results': list(domains)})
    return JsonResponse({'results': []})


def home(request):
    return render(request, 'home.html')

def upload_csv(request):
    if request.method == 'POST':
        # Handle Student CSV
        student_csv_file = request.FILES.get('student_file')
        if student_csv_file:
            student_data = csv.reader(student_csv_file.read().decode('utf-8').splitlines())
            next(student_data, None)  # Skip the header row
            for row in student_data:
                try:
                    name, usn, section = row
                    Student.objects.create(name=name, usn=usn, section=section.lower())
                except ValueError:
                    messages.error(request, f"Invalid data in Student CSV: {row}")
                    return redirect(request.path)

        # Handle Faculty CSV
        faculty_csv_file = request.FILES.get('faculty_file')
        if faculty_csv_file:
            faculty_data = csv.reader(faculty_csv_file.read().decode('utf-8').splitlines())
            next(faculty_data, None)  # Skip the header row
            for row in faculty_data:
                try:
                    name, designation, experience, domain = row
                    Faculty.objects.create(name=name.lower(), designation=designation.lower(), experience=experience, domain=domain.lower())
                except ValueError:
                    messages.error(request, f"Invalid data in Faculty CSV: {row}")
                    return redirect(request.path)

        # Success message
        messages.success(request, 'CSV files processed successfully and data saved to the database.')
        return redirect('admin:index')  # Redirect to the Django admin index

    return render(request, 'admin/upload_csv.html')  # Ensure this template exists


def create_group(request):
    if request.method == 'POST':
        form = GroupCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Group created successfully!')
            return redirect('create_group')
    else:
        form = GroupCreationForm()

    return render(request, 'create_group.html', {'form': form})

def upload_project(request):
    if request.method == 'POST':
        form = ProjectFileForm(request.POST, request.FILES)  # Bind form data and file data
        storage = get_messages(request)
        for _ in storage:
            pass
        if form.is_valid():
            batch_number = form.cleaned_data['batch_number']  # Extract the batch number from the form
            file_type = form.cleaned_data['file_type']
            review_type = form.cleaned_data['review_type']
            project_file = request.FILES.get('project_file')  # Get the uploaded file

            # Validate the file type
            if file_type == 'PPT':
                allowed_mime_types = ['application/vnd.ms-powerpoint', 
                                      'application/vnd.openxmlformats-officedocument.presentationml.presentation']
                mime_type, _ = mimetypes.guess_type(project_file.name)
                
                if mime_type not in allowed_mime_types:
                    messages.error(request, 'Uploaded file type does not match the selected file type (PPT).')
                    return redirect('upload_project')
            
            try:
                # Look for the group with the given batch number
                group = Group.objects.get(batch_number=batch_number)
                # If group is found, update the project file
                
                ext = project_file.name.split('.')[-1]
                new_filename = f"{batch_number}-{review_type}.{ext}"
                project_file.name = new_filename
           
                if file_type=='PPT':
                    if review_type == 'Review-1':
                        group.project_review1_ppt = project_file
                    elif review_type == 'Review-2':
                        group.project_review2_ppt = project_file
                    elif review_type == 'Review-3':
                        group.project_review3_ppt = project_file
                    elif review_type == 'Review-4':
                        group.project_review4_ppt = project_file
                    else:
                        group.project_review5_ppt = project_file
                else:
                    group.project_report = project_file
                group.save()  # Save the updated group details
                messages.success(request, f'Project for batch {batch_number} uploaded successfully!')
                return redirect('upload_project')  # Redirect after successful upload

            except Group.DoesNotExist:
                # If the group does not exist, return an error
                messages.error(request, f'Group with batch number {batch_number} does not exist.')

        else:
            # Handle form validation errors
            messages.error(request, "Invalid form submission.")
            print(form.errors)  # Print form errors for debugging (optional)
    
    else:
        form = ProjectFileForm()

    return render(request, 'upload_project.html', {'form': form})

@csrf_exempt
def search_members(request):
    if request.is_ajax() and request.method == 'GET':
        query = request.GET.get('q', '')
        if query:
            # Filter students by name or USN containing the search query
            students = Student.objects.filter(name__icontains=query) | Student.objects.filter(usn__icontains=query)
            results = [
                {'id': student.id, 'name': f"{student.name} ({student.usn})"} 
                for student in students
            ]
        else:
            results = []
        return JsonResponse({'results': results})
    return JsonResponse({'results': []})

def student_login(request):
    if request.method == 'POST':
        form = StudentLoginForm(request.POST)
        storage = get_messages(request)
        for _ in storage:
            pass
        if form.is_valid():
            usn = form.cleaned_data['usn']
            password = form.cleaned_data['password']
            
            try:
                # Authenticate student using the Student model
                student = Student.objects.get(usn=usn, password=password)
                # Store student info in session
                request.session['student_usn'] = student.usn
                return redirect('student_dashboard')
            except Student.DoesNotExist:
                messages.error(request, 'Invalid USN or password')
    else:
        form = StudentLoginForm()
    return render(request, 'student_login.html', {'form': form})

def guide_login(request):
    if request.method == 'POST':
        form = FacultyLoginForm(request.POST)
        storage = get_messages(request)
        for _ in storage:
            pass
        if form.is_valid():
            name = form.cleaned_data['name']
            password = form.cleaned_data['password']
            
            try:
                faculty = Faculty.objects.get(name=name,password=password)
                request.session['faculty_name'] = faculty.name
                return redirect('guide_dashboard')
            except Faculty.DoesNotExist:
                messages.error(request, 'Invalid name or password.')
    else:
        form = FacultyLoginForm()
    return render(request, 'guide_login.html', {'form': form})

def student_dashboard(request):
    # Check if student is logged in
    if 'student_usn' not in request.session:
        return redirect('student_login')
    # Fetch student information using USN from session
    student_usn = request.session['student_usn']
    try:
        student = Student.objects.get(usn=student_usn)  # Query the student based on USN
        student_name = student.name  # Assuming `name` is a field in the Student model
    except Student.DoesNotExist:
        # Redirect to login if the student doesn't exist
        return redirect('student_login')
    groups = Group.objects.filter(members=student)  # Fetch groups where the student is a member
    
    # Pass student name to the template
    context = {'groups': groups,'student_name': student_name}
    return render(request, 'student_dashboard.html', context)


def view_doc(request):
    student_usn = request.session.get('student_usn')

    # Check if there's a group where the student is the leader
    group = Group.objects.filter(members__usn=student_usn).first()

    review_ppt_fields = [
        'project_review5_ppt',
        'project_review4_ppt',
        'project_review3_ppt',
        'project_review2_ppt',
        'project_review1_ppt',
    ]

    # Get the latest PPT URL
    latest_review_ppt = None
    for field in review_ppt_fields:
        ppt_file = getattr(group, field, None)  # Get the file field value
        if ppt_file:  # Check if file exists
            latest_review_ppt = ppt_file.url  # Get the URL
            break

    if group:
        return render(request, 'view_documents.html', {
            'project_review1_ppt': latest_review_ppt,
            'project_report': group.project_report.url if group.project_report else None,
        })
    else:
        return render(request, 'view_documents.html', {
            'error': 'No documents available for this user.',
        })
    
def student_logout(request):
    # logout(request)
    return redirect('student_login')

def guide_dashboard(request):
    # Retrieve the Faculty instance from the session
    faculty_name = request.session.get('faculty_name')
    try:
        faculty = Faculty.objects.get(name=faculty_name)
    except Faculty.DoesNotExist:
        # Handle the case where the faculty is not found
        messages.error(request, "Invalid faculty. Please log in again.")
        return redirect('guide_login')

    # Get the groups assigned to this guide (Faculty)
    assigned_groups = Group.objects.filter(guide=faculty)
    for group in assigned_groups:
        group.latest_review_ppt = None  # Default to None if no PPT is uploaded

        # Check for the latest review PPT in order
        if group.project_review5_ppt:
            group.latest_review_ppt = group.project_review5_ppt
        elif group.project_review4_ppt:
            group.latest_review_ppt = group.project_review4_ppt
        elif group.project_review3_ppt:
            group.latest_review_ppt = group.project_review3_ppt
        elif group.project_review2_ppt:
            group.latest_review_ppt = group.project_review2_ppt
        elif group.project_review1_ppt:
            group.latest_review_ppt = group.project_review1_ppt

    context = {
        'assigned_groups': assigned_groups,
        'faculty_name': faculty_name,
    }

    return render(request, 'guide_dashboard.html', context)


def view_groups(request):
    # Logic to fetch groups assigned to the guide
    return render(request, 'view_groups.html')

def review_projects(request):
    # Logic to display uploaded projects for review
    return render(request, 'review_projects.html')

def provide_feedback(request):
    # Logic for feedback form and marks allotment
    return render(request, 'provide_feedback.html')

def forgotPassword(request):
    if request.method == 'POST':
        usn = request.POST.get('usn')
        section = request.POST.get('sec')
        password = request.POST.get('password')
        password_confirm = request.POST.get('confirm')

        if password == password_confirm:
            try:
                # Retrieve the student using USN and Section
                student = Student.objects.get(usn=usn, section=section)
                # Update the password securely
                student.password = password
                student.save()
                messages.success(request, "Password updated successfully.")
                return redirect('student_login')  # Redirect to login URL pattern
            except Student.DoesNotExist:
                messages.error(request, "Invalid USN or Section.")
        else:
            messages.error(request, "Passwords do not match.")

    return render(request, 'forgotPassword.html')

def guide_forgotPassword(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        password = request.POST.get('password')
        password_confirm = request.POST.get('confirm')

        if password == password_confirm:
            try:
                faculty = Faculty.objects.get(name=name)
                faculty.password = password
                faculty.save()
                messages.success(request, "Password updated successfully.")
                return redirect('guide_login')
            except Faculty.DoesNotExist:
                messages.error(request, "Invalid Name.")
        else:
            messages.error(request, "Passwords do not match.")

    return render(request, 'guide_forgotPassword.html')


def change_password(request):
    if request.session.get('student_usn'):
        return redirect('forgotPassword')
    else:
        return redirect('guide_forgotPassword')
    
def notifications(request):
    # Fetch the initial data for rendering the template
    Updata_data = (Update.objects.all()).order_by('-timestamp')
    attachments_data = (Attachment.objects.all())
    
    # Get the currently logged-in student (assuming the user is logged in)
    usn = request.session.get('student_usn')
    
    # Fetch the Student instance related to the logged-in user
    student = Student.objects.get(usn=usn)  # Adjust field as needed
    print(student)
    # Search for the group where the student is either the leader or a member
    group = Group.objects.filter(members=student).first()  # Use .first() to get the first matching group
    print(group)
    # if not group:
    #     # Handle the case where no group is found for the student
    #     raise ValueError("The student is not part of any group.")
    if group:
    # Get the batch number from the group
        batch_number = group.batch_number
        print(batch_number)
        # Use batch_number to filter GuideNotification objects
        if batch_number:
            guide_noti = GuideNotification.objects.filter(batch_number=batch_number).order_by('-timestamp')

            # Mark updates as seen
            for noti in guide_noti:
                if not noti.is_seen:  # Check if is_seen is False
                    noti.is_seen = True  # Set is_seen to True
                    noti.save()

            # Retrieve the attachments for the filtered GuideNotifications
            guide_attachments = []
            for notification in guide_noti:
                attachments = notification.guide_attachments.all()  # Access related attachments
                guide_attachments.extend(attachments)

            # Add the guide attachments to the context
            context = {
                'data': Updata_data,
                'attachments': attachments_data,
                'guide_notifications': guide_noti,
                'guide_attachments': guide_attachments
            }
    else:
        # If no batch_number is provided, just render the basic context
        context = {
            'data': Updata_data,
            'attachments': attachments_data
        }

    # Mark updates as seen
    for update in Updata_data:
        if not update.is_seen:
            update.is_seen = True
            update.save()

    response = render(request, 'notifications.html', context)
    return response

def send_push_notification(subscription_info, message_body):
    print(message_body)
    try:
        webpush(
            subscription_info={
                "endpoint": subscription_info.endpoint,
                "keys": {
                    "p256dh": subscription_info.keys_p256dh,
                    "auth": subscription_info.keys_auth,
                },
            },
            data=message_body,
            vapid_private_key=settings.VAPID_PRIVATE_KEY,
            vapid_claims=settings.VAPID_CLAIMS,
        )
    except WebPushException as ex:
        print(f"WebPush failed: {ex}")

def send_notifications_to_all(message_body):
    subscriptions = PushSubscription.objects.all()
    for subscription in subscriptions:
        send_push_notification(subscription, message_body)


def notify(request):
    if request.method == "POST":
        batch_number = request.POST.get("batch_number")
        title = request.POST.get("title")
        content = request.POST.get("content")
        attachments = request.FILES.getlist("attachments")  # Multiple files

        try:
            # Get the group based on the batch number
            group = Group.objects.get(batch_number=batch_number)

            # Create the GuideNotification
            notification = GuideNotification.objects.create(
                name=request.session.get('faculty_name'),  # Assuming the logged-in user is a Faculty
                batch_number=batch_number,
                title=title,
                content=content,
            )

            # Save each attachment in the related model
            for file in attachments:
                GuideAttachments.objects.create(notification=notification, file=file)

            # Fetch group members and send notifications
            members = group.members.all()
            for member in members:
                subscription = PushSubscription.objects.filter(usn=member.usn).first()
                if subscription:
                    message_body = f"New Notification: {title}\n{content}"
                    send_push_notification(subscription, message_body)

            messages.success(request, 'Message has been sent successfully!')
            return redirect('notify')
        except Group.DoesNotExist:
            return JsonResponse({"error": "Invalid batch number."}, status=400)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)
    else:
        groups = Group.objects.all()
        return render(request, "guide_notification.html", {"groups": groups})
