from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import ugettext as _ 
from django.contrib.auth.signals import user_logged_in

from functools import reduce
from profiles.models import Job
# or 
# import functools


class MatchList(models.Model):
    """Model definition for MatchList."""

    user = models.ForeignKey(User, verbose_name=_("Main User"), related_name="main_user", on_delete=models.CASCADE)
    match = models.ForeignKey(User, verbose_name=_("Match User"), related_name="match_user", on_delete=models.CASCADE)
    read = models.BooleanField(_("Read"), default=False)
    read_at = models.DateField(_("Read at"), auto_now=False, auto_now_add=False, null=True, blank=True)
    timestamp = models.DateTimeField(_("Timestamp"), auto_now=False, auto_now_add=True)
    updated = models.DateTimeField(_("Updated"), auto_now=True, auto_now_add=False)

    class Meta:
        """Meta definition for MatchList."""

        ordering = ['-updated', '-timestamp']
        verbose_name = 'MatchList'
        verbose_name_plural = 'MatchLists'

    def __str__(self):
        """Unicode representation of MatchList."""
        return str(self.match.username)


# after each loogin it will look for a match and create one
def login_user_mataches(sender, user, request, **kwargs):
    obj = Match.objects.filter(from_user=user)
    for abc in obj:
        if abc.to_user != user:
            if Match.objects.good_match(abc.to_user, user):
                add_to_list, created = MatchList.objects.get_or_create(user=user, match=abc.to_user)
    obj2 = Match.objects.filter(to_user=user)
    for abc in obj2:
        if abc.from_user != user:
            if Match.objects.good_match(abc.from_user, user):
                add_to_list, created = MatchList.objects.get_or_create(user=user, match=abc.from_user)
    request.session["new_matches_count"] = MatchList.objects.filter(user=user).filter(read=False).count()

user_logged_in.connect(login_user_mataches)


class MatchManager(models.Manager):
    # here the ordere for user it doesn't matter
    def are_matched(self, user1, user2):
        if self.filter(from_user=user1, to_user=user2).count()>0:
            obj = Match.objects.get(from_user=user1, to_user=user2)
            perc = obj.percent * 100
            return perc 
        if self.filter(from_user=user2, to_user=user1).count()>0:
            obj = Match.objects.get(from_user=user2, to_user=user1)
            perc = obj.percent * 100
            return perc
        else:
            return False
    
    def good_match(self, user1, user2):
        # if you wanna do some how advance to match every user and find it's average so do this code 
        obj = Match.objects.all()
        per = [] 
        for i in obj:
            per.append(i.percent)
        avg_per = reduce(lambda x,y: x+y, per)/len(per)
        # because it's return percent so I can use > or <
        if self.are_matched(user1, user2) >= avg_per:
            print("Matched")
            return True
        else:
            print("Not matched")
            return False


class Match(models.Model):
    """Model definition for Match."""

    to_user = models.ForeignKey(User, verbose_name=_("To user"), on_delete=models.CASCADE, related_name="match")
    from_user = models.ForeignKey(User, verbose_name=_("From User"), on_delete=models.CASCADE, related_name="match2")
    percent = models.DecimalField(_("Percent"), max_digits=5, decimal_places=2, default=.75)
    good_match = models.BooleanField(_("Good Match"), default=True)
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


class JobMatch(models.Model):
    """Model definition for JobMatch."""

    user = models.ForeignKey(User, verbose_name=_("User"), on_delete=models.CASCADE)
    job  = models.ForeignKey(Job, verbose_name=_("Job"), on_delete=models.CASCADE, null=True, blank=True)
    show = models.BooleanField(_("Show"), default=True)
    
    class Meta:
        """Meta definition for JobMatch."""

        verbose_name = 'JobMatch'
        verbose_name_plural = 'JobMatchs'

    def __str__(self):
        """Unicode representation of JobMatch."""
        return self.job.position
