from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from connections.models import Connection

@login_required
def dashboard(request):
    user = request.user
    profile = user.profile

    print(f"DEBUG: User = {user.email} | Role = {user.role}")  # ← For debugging

    if user.role == 'student':
        active = Connection.objects.filter(student=user, status='accepted')
        pending = Connection.objects.filter(student=user, status='pending')
        is_student = True
        is_alumni = False
    else:
        active = Connection.objects.filter(mentor=user, status='accepted')
        pending = Connection.objects.filter(mentor=user, status='pending')
        is_student = False
        is_alumni = True

    print(f"DEBUG: Pending Requests for this user = {pending.count()}")  # ← Important

    context = {
        'full_name': profile.full_name or user.email.split('@')[0],
        'user_role': user.role,
        'active_mentorships': active,
        'pending_requests': pending,
        'is_student': is_student,
        'is_alumni': is_alumni,
    }


@login_required
def dashboard(request):
    user = request.user
    profile = user.profile

    # Show pending requests for admin as well (for testing)
    if user.role in ['admin', 'alumni', 'faculty']:
        active = Connection.objects.filter(mentor=user, status='accepted')
        pending = Connection.objects.filter(mentor=user, status='pending')
        is_student = False
        is_alumni = True
    else:
        active = Connection.objects.filter(student=user, status='accepted')
        pending = Connection.objects.filter(student=user, status='pending')
        is_student = True
        is_alumni = False

    context = {
        'full_name': profile.full_name or user.email.split('@')[0],
        'user_role': user.role,
        'active_mentorships': active,
        'pending_requests': pending,
        'is_student': is_student,
        'is_alumni': is_alumni,
    }

    # return render(request, 'dashboard/dashboard.html', context)
    return render(request, 'dashboard/dashboard.html', context)