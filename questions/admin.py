from django.contrib import admin
from .models import Question, Answer


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    class Meta:
        model = Question


@admin.register(Answer)
class AnswerAdmin(admin.ModelAdmin):
    class Meta:
        model = Answer



