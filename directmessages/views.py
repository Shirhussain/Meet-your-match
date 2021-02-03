from django.shortcuts import render, Http404, get_object_or_404, HttpResponseRedirect
from django.urls import reverse
from django.contrib import messages
import datetime

from .models import DirectMessage
from .forms import DirectMessageForm, ReplyForm


def direct_message_view(request, id):
    message = get_object_or_404(DirectMessage, id=id)
    if not message.sender != request.user or message.receiver != request.user:
        raise Http404

    if not message.read:
        message.read = True
        message.read_at = datetime.datetime.now()
        message.save()

    context = {
        'message': message
    }
    return render(request, "directmessages/view.html", context)

def compose(request):
    # when you are using HTML tag in view like here so it has some down side as well
    # when you are in production so every time you have to manually restart the server
    title = "<h1>Compose</h1>"
    form = DirectMessageForm(request.POST or None)
    if form.is_valid():
        send_message = form.save(commit=False)
        send_message.sender = request.user
        send_message.sent = datetime.datetime.now()
        send_message.save()
        messages.success(request, "your messages has been send")
        return HttpResponseRedirect(reverse("directmessages:inbox"))

    context = {
        'form': form,
        'title': title,
    }
    return render(request, "directmessages/compose.html", context)

def reply(request, id):
    parent_id = id 
    parent = get_object_or_404(DirectMessage, id=parent_id)
    title = f"<h1>Reply: <small> {parent.subject} from {parent.sender}</small> </h1>"
    # if you want to delete teh parent do the line below 
    # parent.delete()
    
    form = ReplyForm(request.POST or None)
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
        messages.success(request, f"you have replied to {parent.sender} successfully")
        return HttpResponseRedirect(reverse("directmessages:view", kwargs={'id': id}))
    
    context = {
        'form': form,
        'title': title,
    }
    return render(request, "directmessages/compose.html", context)

def inbox(request):
    messages_in_inbox = DirectMessage.objects.filter(receiver=request.user)
    
    direct_messages = DirectMessage.objects.get_num_unread_messages(request.user)
    request.session['number_of_messages'] = direct_messages

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