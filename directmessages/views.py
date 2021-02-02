from django.shortcuts import render, Http404, get_object_or_404
import datetime

from .models import DirectMessage
from .forms import DirectMessageForm


def direct_message_view(request, id):
    message = get_object_or_404(DirectMessage, id=id)
    if not message.sender != request.user or message.receiver != request.user:
        raise Http404

    if not message.read:
        message.read = datetime.datetime.now()
        message.save()

    context = {
        'message': message
    }
    return render(request, "directmessages/view.html", context)

def compose(request):
    form = DirectMessageForm(request.POST or None)
    if form.is_valid():
        send_message = form.save(commit=False)
        send_message.sender = request.user
        send_message.sent = datetime.datetime.now()
        send_message.save()
    context = {
        'form': form,
    }
    return render(request, "directmessages/compose.html", context)

def reply(request, id):
    parent_id = id 
    parent = get_object_or_404(DirectMessage, id=parent_id)
    # if you want to delete teh parent do the line below 
    # parent.delete()
    
    form = DirectMessageForm(request.POST or None)
    if form.is_valid():
        send_message = form.save(commit=False)
        send_message.sender = request.user 
        send_message.receiver = parent.sender
        send_message.subject = "Re: " + parent.subject
        send_message.sent = datetime.datetime.now()
        send_message.parent = parent
        send_message.save()
        parent.replied = True
        parent.save()
    
    context = {
        'form': form,
    }
    return render(request, "directmessages/compose.html", context)

def inbox(request):
    messages_in_inbox = DirectMessage.objects.filter(receiver=request.user)
    request.session['number_of_messages'] = len(messages_in_inbox)

    context = {
        'messages_in_inbox': messages_in_inbox,
    }
    return render(request, "directmessages/inbox.html", context)

def sent(request):
    messages_sent = DirectMessage.objects.filter(sender=request.user)
    context = {
        'messages_sent': messages_sent
    }
    return render(request, "directmessages/sent.html", context)