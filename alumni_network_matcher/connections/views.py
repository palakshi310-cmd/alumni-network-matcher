from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Connection
from profiles.models import Profile

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Connection

@login_required
def my_connections(request):
    user = request.user

    if user.role == 'student':
        active = Connection.objects.filter(student=user, status='accepted')
        pending_sent = Connection.objects.filter(student=user, status='pending')
        rejected = Connection.objects.filter(student=user, status='rejected')
        pending_received = []
    else:
        active = Connection.objects.filter(mentor=user, status='accepted')
        pending_sent = []
        rejected = []
        pending_received = Connection.objects.filter(mentor=user, status='pending')

    context = {
        'active_connections': active,
        'pending_sent': pending_sent,
        'rejected_requests': rejected,
        'pending_received': pending_received,
        'is_alumni': user.role != 'student',
    }
    return render(request, 'connections/my_connections.html', context)


@login_required
def send_connection_request(request, mentor_id):
    mentor_profile = get_object_or_404(Profile, pk=mentor_id, user__role='alumni')
    
    if mentor_profile.user == request.user:
        messages.error(request, "You cannot send request to yourself.")
        return redirect('find_mentors')

    if Connection.objects.filter(student=request.user, mentor=mentor_profile.user).exists():
        messages.warning(request, "Request already sent.")
        return redirect('find_mentors')

    if request.method == 'POST':
        message = request.POST.get('message', '')
        Connection.objects.create(
            student=request.user,
            mentor=mentor_profile.user,
            message=message
        )
        messages.success(request, f"Request sent to {mentor_profile.full_name}!")
        return redirect('my_connections')
    
    return render(request, 'connections/send_request.html', {'mentor': mentor_profile})
@login_required
def handle_request(request, connection_id, action):
    connection = get_object_or_404(Connection, pk=connection_id, mentor=request.user)
    
    if action == 'accept':
        connection.status = 'accepted'
        messages.success(request, "Mentorship request accepted!")
    elif action == 'reject':
        connection.status = 'rejected'
        messages.success(request, "Mentorship request rejected.")
    
    connection.save()
    return redirect('my_connections')