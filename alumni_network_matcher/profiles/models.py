from django.db import models
from django.conf import settings

class Profile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='profile')

    full_name = models.CharField(max_length=255, blank=True)
    profile_picture = models.ImageField(upload_to='profile_pics/', blank=True, null=True)
    bio = models.TextField(blank=True, null=True)
    location = models.CharField(max_length=100, blank=True)

    # Academic & Professional
    department = models.CharField(max_length=100, blank=True)
    batch_year = models.IntegerField(blank=True, null=True)
    current_status = models.CharField(max_length=100, blank=True)

    current_company = models.CharField(max_length=200, blank=True, null=True)
    current_job_title = models.CharField(max_length=150, blank=True, null=True)
    experience_years = models.PositiveIntegerField(default=0)

    skills = models.TextField(blank=True, help_text="Comma separated skills")
    achievements = models.TextField(blank=True)
    mentorship_areas = models.TextField(blank=True, help_text="Areas you can mentor in")

    is_available_for_mentorship = models.BooleanField(default=True)
    linkedin_url = models.URLField(blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.full_name or self.user.email}"

    def get_combined_text(self):
        """Combine all text for vectorization"""
        text = f"{self.skills} {self.department} {self.bio} {self.mentorship_areas} "
        if self.user.role == 'alumni':
            text += f"{self.current_job_title} {self.current_company} {self.achievements}"
        return text.lower()