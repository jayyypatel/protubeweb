from django.shortcuts import render
from chat.models import Thread
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required

@login_required(login_url='auth_system:login_user')
def messages_page(request):
    threads = Thread.objects.by_user(user=request.user).prefetch_related('chatmessage_thread').order_by('timestamp')
    print(get_user_model().objects.get(id=2))
    context = {
        'Threads': threads
    }
    return render(request, 'chat/messages.html', context)