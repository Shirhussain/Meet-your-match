from django.shortcuts import render
from .models import Question, Answer

def all_question(request):
    questions = Question.objects.all()
    context = {
        'questions': questions,
    }
    return render(request, "questions/all.html", context)