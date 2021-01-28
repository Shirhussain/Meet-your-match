from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import ugettext as _

class Question(models.Model):
    """Model definition for Question."""

    user = models.ForeignKey(User, verbose_name=_("User"), on_delete=models.CASCADE)
    question = models.CharField(_("Questions"), max_length=150)
    timestamp = models.DateTimeField(_("Timestamp"), auto_now=False, auto_now_add=True)
    updated = models.DateTimeField(_("Updated"), auto_now=True, auto_now_add=False)
    class Meta:
        """Meta definition for Question."""

        verbose_name = 'Question'
        verbose_name_plural = 'Questions'

    def __str__(self):
        """Unicode representation of Question."""
        return self.question

class Answer(models.Model):
    """Model definition for Answer."""

    question = models.ForeignKey(Question, verbose_name=_("Question"), on_delete=models.CASCADE)
    answer = models.CharField(_("Answer"), max_length=150)
    timestamp = models.DateTimeField(_("Timestamp"), auto_now=False, auto_now_add=True)
    updated = models.DateTimeField(_("Updated"), auto_now=True, auto_now_add=False)

    class Meta:
        """Meta definition for Answer."""

        verbose_name = 'Answer'
        verbose_name_plural = 'Answers'

    def __str__(self):
        """Unicode representation of Answer."""
        return self.answer


class UserAnswer(models.Model):
    """Model definition for UserAnswer."""

    user = models.ForeignKey(User, verbose_name=_("User"), on_delete=models.CASCADE)
    question = models.ForeignKey(Question, verbose_name=_("Question"), on_delete=models.CASCADE)
    answer = models.ForeignKey(Answer, verbose_name=_("Answer"), on_delete=models.CASCADE, blank=True, null=True)
    importance_level = models.CharField(_("Importance Level"), max_length=50, default='Somewhat Important', blank=True, null=True)
    points = models.IntegerField(_("Points"), default='20')
    timestamp = models.DateTimeField(_("Timestamp"), auto_now=False, auto_now_add=True)
    updated = models.DateTimeField(_("Updated"), auto_now=True, auto_now_add=False)

    class Meta:
        """Meta definition for UserAnswer."""

        verbose_name = 'UserAnswer'
        verbose_name_plural = 'UserAnswers'

    def __str__(self):
        """Unicode representation of UserAnswer."""
        return str(self.answer.answer)


class MatchAnswer(models.Model):
    """Model definition for MatchAnswer."""

    user = models.ForeignKey(User, verbose_name=_("User"), on_delete=models.CASCADE)
    question = models.ForeignKey(Question, verbose_name=_("Question"), on_delete=models.CASCADE)
    answer = models.ForeignKey(Answer, verbose_name=_("Answer"), on_delete=models.CASCADE, blank=True, null=True)
    importance_level = models.CharField(_("Importance Level"), max_length=50, default='Somewhat Important', blank=True, null=True)
    points = models.IntegerField(_("Points"), default='20')
    timestamp = models.DateTimeField(_("Timestamp"), auto_now=False, auto_now_add=True)
    updated = models.DateTimeField(_("Updated"), auto_now=True, auto_now_add=False)

    class Meta:
        """Meta definition for MatchAnswer."""

        verbose_name = 'MatchAnswer'
        verbose_name_plural = 'MatchAnswers'

    def __str__(self):
        """Unicode representation of MatchAnswer."""
        return self.answer.answer
