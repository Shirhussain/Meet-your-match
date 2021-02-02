from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import ugettext as _ 
from django.contrib.auth.signals import user_logged_in
from django.urls import reverse

class DirectMessage(models.Model):
    """Model definition for DirectMessage."""

    subject = models.CharField(_("Subject"), max_length=150)
    body = models.CharField(_("Body"), max_length=3000)
    sender = models.ForeignKey(User, verbose_name=_("Sender"), 
                                related_name="sent_direct_messages",
                                on_delete=models.CASCADE,
                                null=True,
                                blank=True
                                )
    receiver = models.ForeignKey(User, verbose_name=_("Receiver"), 
                                on_delete=models.CASCADE,
                                related_name="received_direct_messages",
                                null=True,
                                blank=True
                                )
    sent = models.DateTimeField(_("Sent date"), auto_now=False, auto_now_add=False, null=True, blank=True)
    read = models.DateTimeField(_("Read date"), auto_now=False, auto_now_add=False, null=True, blank=True)
    parent = models.ForeignKey('self', verbose_name=_("Parent"), on_delete=models.CASCADE, null=True, blank=True)
    replied = models.BooleanField(_("Replied"), default=False)

    class Meta:
        """Meta definition for DirectMessage."""

        verbose_name = 'DirectMessage'
        verbose_name_plural = 'DirectMessages'

    def __str__(self):
        """Unicode representation of DirectMessage."""
        return self.subject
    
    def get_absolute_url(self):
        return reverse("directmessages:view", kwargs={"id": self.pk})
    
    

def set_messages_in_session(sender, user, request, **kwargs):
    direct_messages = DirectMessage.objects.filter(receiver=user)
    request.session['number_of_messages'] = len(direct_messages)

user_logged_in.connect(set_messages_in_session)