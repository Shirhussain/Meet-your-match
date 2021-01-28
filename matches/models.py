from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import ugettext as _ 


class MatchManager(models.Manager):
    def are_matched(self, user1, user2):
        if self.filter(from_user=user1, to_user=user2).count()>0:
            obj = Match.objects.get(from_user=user1, to_user=user2)
            perc = obj.percent
            return perc 
        if self.filter(from_user=user2, to_user=user1).count()>0:
            obj = Match.objects.get(from_user=user2, to_user=user1)
            perc = obj.percent
            return perc
        else:
            return False

class Match(models.Model):
    """Model definition for Match."""

    to_user = models.ForeignKey(User, verbose_name=_("To user"), on_delete=models.CASCADE, related_name="match")
    from_user = models.ForeignKey(User, verbose_name=_("From User"), on_delete=models.CASCADE, related_name="match2")
    percent = models.DecimalField(_("Percent"), max_digits=5, decimal_places=2, default=.75)
    timestamp = models.DateTimeField(_("Timestamp"), auto_now=False, auto_now_add=True)
    updated = models.DateTimeField(_("Updated"), auto_now=True, auto_now_add=False)

    objects = MatchManager()

    class Meta:
        """Meta definition for Match."""

        verbose_name = 'Match'
        verbose_name_plural = 'Matches'

    def __str__(self):
        """Unicode representation of Match."""
        return self.percent
