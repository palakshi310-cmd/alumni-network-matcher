from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
from profiles.models import Profile

def get_mentor_recommendations(student_profile, top_n=10):
    """
    Returns top matching alumni with match scores using Cosine Similarity
    """
    # Get all available alumni
    alumni = Profile.objects.filter(
        user__role='alumni',
        is_available_for_mentorship=True
    ).select_related('user')

    if not alumni.exists():
        return []

    # Prepare documents for vectorization
    documents = [alumni_profile.get_combined_text() for alumni_profile in alumni]
    documents.insert(0, student_profile.get_combined_text())  # Student's profile at index 0

    # Vectorization
    vectorizer = TfidfVectorizer(stop_words='english')
    tfidf_matrix = vectorizer.fit_transform(documents)

    # Calculate similarity
    cosine_sim = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:])

    # Get similarity scores
    similarity_scores = cosine_sim[0]

    # Create list of (alumni, score)
    recommendations = []
    for idx, score in enumerate(similarity_scores):
        alumni_profile = alumni[idx]
        recommendations.append({
            'profile': alumni_profile,
            'match_score': round(float(score * 100), 1),
            'reason': get_match_reason(student_profile, alumni_profile)
        })

    # Sort by match score (highest first)
    recommendations.sort(key=lambda x: x['match_score'], reverse=True)

    return recommendations[:top_n]


def get_match_reason(student, alumni):
    """Generate simple explanation for match"""
    reasons = []
    if student.department and student.department == alumni.department:
        reasons.append(f"Same Department: {student.department}")
    if student.skills and alumni.skills:
        common_skills = set(student.skills.lower().split(',')) & set(alumni.skills.lower().split(','))
        if common_skills:
            reasons.append(f"Shared Skills: {list(common_skills)[:2]}")
    if alumni.current_job_title:
        reasons.append(f"Current Role: {alumni.current_job_title}")
    
    return " | ".join(reasons[:2]) or "Good overall match"