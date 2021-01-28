from django.shortcuts import render
from django.contrib import messages
from django.contrib.auth.models import User
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from .models import Question, Answer, UserAnswer, MatchAnswer

# Mandatory = 300 
# Very important = 100
# somewhat important = 20 
# Not important = 0 

def assign_points(query):
    if query == 'Mandatory':
        return 300
    elif query == 'Very Important':
        return 100
    elif query == 'Somewhat Important':
        return 20 
    else:
        return 0 

def all_question(request):
    questions = Question.objects.all()
    page = request.GET.get('page', 1)
    importance_level = ['Mandatory', 'Very Important', 'Somewhat Important', 'Not Important']

    paginator = Paginator(questions, 2)
    try:
        questions = paginator.page(page)
    except PageNotAnInteger:
        questions = paginator.page(1)
    except EmptyPage:
        questions = paginator.page(paginator.num_pages)

    if request.method == "POST":
        user = User.objects.get(username=request.user)
        question_id = request.POST['question_id']
        question = Question.objects.get(id=question_id)
        # user_answer 
        answer_form = request.POST['answer']
        importance_level = request.POST['importance_level']
        # user match answer 
        match_answer_form = request.POST['match_answer']
        match_importance_level = request.POST['match_importance_level']

        # user answer
        answer = Answer.objects.get(question=question, answer = answer_form)
        # here in line below id don't wanna put answer=answer because everytime we wanna change our answer 
        # i will have a new instance created which i don't want that 
        answered, created = UserAnswer.objects.get_or_create(user=user, question=question)
        answered.answer = answer 
        answered.importance_level = importance_level
        points = assign_points(importance_level)
        answered.points = points
        answered.save()

        # user match answer
        match_answer = Answer.objects.get(question=question, answer=match_answer_form)
        answered, created = MatchAnswer.objects.get_or_create(user=user, question = question)
        answered.answer = match_answer
        answered.importance_level = match_importance_level
        points = assign_points(match_importance_level)
        answered.points = points 
        answered.save()
        messages.success(request, "your answered has been saved successfully.")

    context = {
        'questions': questions,
        'importance_level': importance_level
    }
    return render(request, "questions/all.html", context)