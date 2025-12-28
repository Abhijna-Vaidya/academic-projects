from django.utils.text import get_valid_filename
from django.db import models
from django.contrib.auth.models import User
import os
from django.conf import settings

FINAL_REPORT_DIR = os.path.join(settings.MEDIA_ROOT, 'uploads/final_reports')
FINAL_PPT_DIR = os.path.join(settings.MEDIA_ROOT, 'uploads/review_ppts')
PPT_DIR = os.path.join(settings.MEDIA_ROOT, 'uploads/notification_docs/ppts')
WORD_DIR = os.path.join(settings.MEDIA_ROOT, 'uploads/notification_docs/word_docs')

import os
from django.conf import settings

def upload_to(instance, filename):
    # Extract the file extension
    ext = filename.split('.')[-1].lower()
    # Define directories for PPTs and reports
    if ext == 'pptx':
        directory = FINAL_PPT_DIR 
    else:
        directory = FINAL_REPORT_DIR

    # Ensure the directory exists
    full_directory_path = os.path.join(settings.MEDIA_ROOT, directory)
    os.makedirs(full_directory_path, exist_ok=True)

    # Return the relative path for Django to store the file
    return os.path.join(directory, filename)


def notification_docs(instance,filename):
    if not filename:
        return None

    filename = get_valid_filename(filename)  # Sanitize filename
    name, ext = os.path.splitext(filename)
    ext = ext.lower()

    if ext == '.pptx':
        directory = PPT_DIR
    else:
        directory = WORD_DIR

    # Return only the relative path
    return os.path.join(directory, filename)

   
# Model to store Student details
class Student(models.Model):
    usn = models.CharField(max_length=10, unique=True) 
    name = models.CharField(max_length=100)
    section = models.CharField(max_length=1,default="A")
    password = models.CharField(max_length=10,default="cse")

    def __str__(self):
        return f"{self.name} ({self.usn})"

# Model to store Faculty details
class Faculty(models.Model):
    name = models.CharField(max_length=100)
    experience = models.IntegerField()
    designation = models.CharField(max_length=20)
    domain = models.CharField(max_length=100)
    password = models.CharField(max_length=10,default="cse")

    def __str__(self):
        return f"{self.name}"


class Domain(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name

class Group(models.Model):
    batch_number = models.CharField(max_length=10, unique=True, blank=True)
    leader = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='leader')
    members = models.ManyToManyField(Student, related_name='members')
    domain = models.ForeignKey(Domain, on_delete=models.CASCADE)
    guide = models.ForeignKey(Faculty, on_delete=models.CASCADE,related_name='guide',null=True, blank=True)
    project_review1_ppt = models.FileField(upload_to=upload_to, null=True, blank=True, max_length=500) 
    project_review2_ppt = models.FileField(upload_to=upload_to, null=True, blank=True, max_length=500)  # Field for uploading project file
    project_review3_ppt = models.FileField(upload_to=upload_to, null=True, blank=True, max_length=500)  # Field for uploading project file
    project_review4_ppt = models.FileField(upload_to=upload_to, null=True, blank=True, max_length=500)  # Field for uploading project file
    project_review5_ppt = models.FileField(upload_to=upload_to, null=True, blank=True, max_length=500)  # Field for uploading project file
    project_report = models.FileField(upload_to=upload_to, null=True, blank=True, max_length=500)  
    review_done = models.BooleanField(default=False)

    def __str__(self):
        guide_name = self.guide.name if self.guide else "Not Assigned"
        return f"Group led by {self.leader.name} for {self.domain.name} guided by {guide_name}"
    
    def save(self, *args, **kwargs):
        # Automatically assign batch number if it's not already assigned
        if not self.batch_number:
            self.batch_number = self.generate_batch_number()

        super().save(*args, **kwargs)
        

    def generate_batch_number(self):
        # Retrieve the last group in the database
        last_group = Group.objects.all().order_by('id').last()
        
        if last_group and last_group.batch_number and last_group.batch_number.startswith('B'):
            # Extract the numeric part of the batch number and increment it
            last_number = int(last_group.batch_number[1:])  # Remove the "B" prefix and convert to integer
            new_batch_number = f"B{last_number + 1}"
        else:
            # If there are no previous groups or no valid batch_number format, start with "B1"
            new_batch_number = "B1"
        
        return new_batch_number
    

class Update(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    is_seen=models.BooleanField(default=False)

    def __str__(self):
        return f"Update from {self.user.username} at {self.timestamp}"
class Attachment(models.Model):
    update = models.ForeignKey(Update, related_name='attachments', on_delete=models.CASCADE)
    file = models.FileField(upload_to=notification_docs, null=True, blank=True, max_length=500)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Attachment for Update {self.update.id}"



def ev_upload_to(instance, filename):
    # Extract the file extension
    ext = filename.split('.')[-1]
    new_filename = f"{instance.group.batch_number}.{ext}"
    
    # Construct the full file path
    file_path = os.path.join(settings.MEDIA_ROOT, 'evaluation_sheets', new_filename)
    
    # Check if the file already exists and delete it
    if os.path.exists(file_path):
        os.remove(file_path)
    
    # Return the new path to save the file
    return os.path.join('evaluation_sheets', new_filename)

class EvaluationSheet(models.Model):
    group = models.ForeignKey(Group, on_delete=models.CASCADE)
    evaluation_file = models.FileField(upload_to=ev_upload_to ,null=True, blank=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Evaluation Sheet for {self.group.batch_number}"


class PushSubscription(models.Model):
    # Unique endpoint for push notifications
    endpoint = models.TextField() 
    # Encryption key for payload
    keys_p256dh = models.CharField(max_length=255)
    # Authentication key
    keys_auth = models.CharField(max_length=255)
    # Reference to the student's USN
    usn = models.CharField(max_length=20,unique=True)


class GuideNotification(models.Model):
    name=models.CharField(max_length=50)
    batch_number=models.CharField(max_length=10)
    title = models.CharField(max_length=200)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    is_seen=models.BooleanField(default=False)

class GuideAttachments(models.Model):
    notification = models.ForeignKey(GuideNotification, related_name='guide_attachments', on_delete=models.CASCADE)
    file = models.FileField(upload_to=notification_docs, null=True, blank=True)