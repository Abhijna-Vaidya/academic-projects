# forms.py

from django import forms
from .models import Student, Group, Domain, Faculty, EvaluationSheet
from django.db.models import Q
from django_select2.forms import Select2MultipleWidget,Select2Widget

class CSVUploadForm(forms.Form):
    student_csv = forms.FileField(label='Upload Student CSV')
    faculty_csv = forms.FileField(label='Upload Faculty CSV')

class GroupCreationForm(forms.ModelForm):
    leader = forms.ModelChoiceField(
        queryset=Student.objects.filter(members__isnull=True),
        widget=Select2Widget(attrs={'data-url': '/student-autocomplete/'}),
        label="Group Leader"
    )

    domain = forms.ModelChoiceField(
        queryset=Domain.objects.all(),
        widget=Select2Widget(attrs={'data-url': '/domain-autocomplete/'}),
        label="Choose Domain"
    )

    member_1 = forms.ModelChoiceField(
        queryset=Student.objects.filter(members__isnull=True),
        widget=forms.Select(attrs={'class': 'form-control'}),
        label="Member 1",
        required=True
    )
    member_2 = forms.ModelChoiceField(
        queryset=Student.objects.filter(members__isnull=True),
        widget=forms.Select(attrs={'class': 'form-control'}),
        label="Member 2",
        required=True
    )
    member_3 = forms.ModelChoiceField(
        queryset=Student.objects.filter(members__isnull=True),
        widget=forms.Select(attrs={'class': 'form-control'}),
        label="Member 3",
        required=True
    )
    member_4 = forms.ModelChoiceField(
        queryset=Student.objects.filter(members__isnull=True),
        widget=forms.Select(attrs={'class': 'form-control'}),
        label="Member 4",
        required=False
    )

    class Meta:
        model = Group
        fields = ['leader', 'domain']
        widgets = {
            'leader': forms.Select(attrs={'class': 'form-control'}),
            'domain': forms.Select(attrs={'class': 'form-control'}),
        }
    
    def save(self, commit=True):
        group = super().save(commit=False)
        if commit:
            group.save()
        # Add members from individual fields
        members = [
            self.cleaned_data.get('member_1'),
            self.cleaned_data.get('member_2'),
            self.cleaned_data.get('member_3'),
            self.cleaned_data.get('member_4'),
        ]
        # Filter out None values and add to ManyToManyField
        group.members.set([member for member in members if member])
        return group

    def clean_members(self):
        members = self.cleaned_data['members']
        leader = self.cleaned_data.get('leader')
        if leader not in members:
            raise forms.ValidationError("The group leader must be a group member.")
        if len(members) < 3 or len(members) > 4:
            raise forms.ValidationError("You must select between 3 and 4 members.")
        return members
        
class GroupAdminForm(forms.ModelForm):
    members = forms.ModelMultipleChoiceField(
        queryset=Student.objects.all(),
        widget=Select2MultipleWidget(attrs={'class': 'select2',
            'data-theme': 'custom',
            'style': 'background-color: black; color: white;'}),
        label='Members'
    )
    
    class Meta:
        model = Group
        fields = '__all__'
    
    def clean_members(self):
        members = self.cleaned_data['members']
        if len(members) < 3 or len(members) > 4:
            raise forms.ValidationError("You must select between 3 and 4 members.")
        return members
    
class ProjectFileForm(forms.Form):
    batch_number = forms.CharField(label="Batch Number")
    review_type = forms.ChoiceField(choices=[("Review-1","Review-1"),("Review-2","Review-2"),("Review-3","Review-3"),("Review-4","Review-4"),("Review-5","Review-5"),("Other","Other")], label='Select Review Type', required=True)
    file_type = forms.ChoiceField(choices= [("PPT","PPT"),("Report","Report")], label='Select an option', required=True)
    project_file = forms.FileField(label="Project File (PDF/PPTX only)")
    
class StudentLoginForm(forms.Form):
    usn = forms.CharField(max_length=10, label="USN", widget=forms.TextInput(attrs={'placeholder': 'Enter your USN'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Enter your Password'}), label="Password")

class FacultyLoginForm(forms.Form):
    name = forms.CharField(max_length=10, label="name", widget=forms.TextInput(attrs={'placeholder': 'Enter your Name'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Enter your Password'}), label="Password")

class EvaluationSheetForm(forms.ModelForm):
    class Meta:
        model = EvaluationSheet
        fields = ['evaluation_file']