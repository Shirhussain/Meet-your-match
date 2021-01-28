from django.contrib import admin
from .models import Question, Answer, UserAnswer, MatchAnswer


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    class Meta:
        model = Question


@admin.register(Answer)
class AnswerAdmin(admin.ModelAdmin):
    class Meta:
        model = Answer


@admin.register(UserAnswer)
class UserAnswerAdmin(admin.ModelAdmin):
    class Meta:
        model = UserAnswer


@admin.register(MatchAnswer)
class MatchAnswerAdmin(admin.ModelAdmin):
    class Meta:
        model = MatchAnswer
