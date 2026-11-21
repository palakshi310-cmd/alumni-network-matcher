from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from profiles.models import Profile
from .utils import get_mentor_recommendations
from connections.models import Connection

@login_required
def find_mentors(request):
    student_profile = request.user.profile
    search_query = request.GET.get('search', '')

    if search_query:
        mentors_qs = Profile.objects.filter(
            user__role='alumni',
            is_available_for_mentorship=True
        ).filter(full_name__icontains=search_query)
    else:
        recommendations = get_mentor_recommendations(student_profile, top_n=12)
        mentors_qs = [rec['profile'] for rec in recommendations]

    # Add connection status for each mentor
    mentors = []
    for mentor in mentors_qs:
        connection = Connection.objects.filter(
            student=request.user, 
            mentor=mentor.user
        ).first()

        mentor.match_score = getattr(mentor, 'match_score', 85)
        mentor.match_reason = getattr(mentor, 'match_reason', '')
        mentor.connection_status = connection.status if connection else None
        mentor.connection = connection
        mentors.append(mentor)

    context = {
        'mentors': mentors,
        'search_query': search_query,
    }
    return render(request, 'matching/find_mentors.html', context)


@login_required
def mentor_detail(request, pk):
    mentor = get_object_or_404(Profile, pk=pk, user__role='alumni')
    context = {'mentor': mentor}
    return render(request, 'matching/mentor_detail.html', context)