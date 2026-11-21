from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from connections.models import Connection
from .models import Message

@login_required
def chat_room(request, connection_id):
    connection = get_object_or_404(Connection, id=connection_id)
    
    # Security: Only participants can chat
    if request.user not in [connection.student, connection.mentor]:
        return redirect('my_connections')

    # Get all messages
    messages = Message.objects.filter(connection=connection)

    if request.method == 'POST':
        content = request.POST.get('content')
        if content:
            Message.objects.create(
                connection=connection,
                sender=request.user,
                receiver=connection.mentor if request.user == connection.student else connection.student,
                content=content
            )
            return redirect('chat_room', connection_id=connection.id)

    context = {
        'connection': connection,
        'messages': messages,
        'other_user': connection.mentor if request.user == connection.student else connection.student,
    }
    return render(request, 'chat/chat_room.html', context)