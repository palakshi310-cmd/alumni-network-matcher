from django import forms
from .models import Profile

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = [
            'full_name', 'profile_picture', 'bio', 'location',
            'department', 'batch_year', 'current_status',
            'current_company', 'current_job_title', 'experience_years',
            'skills', 'achievements', 'mentorship_areas',
            'is_available_for_mentorship', 'linkedin_url'
        ]
        widgets = {
            'bio': forms.Textarea(attrs={'rows': 3, 'class': 'form-control'}),
            'skills': forms.Textarea(attrs={'rows': 2, 'class': 'form-control', 'placeholder': 'Python, Journalism, Video Editing, Anchoring...'}),
            'achievements': forms.Textarea(attrs={'rows': 2, 'class': 'form-control'}),
            'mentorship_areas': forms.Textarea(attrs={'rows': 2, 'class': 'form-control'}),
        }