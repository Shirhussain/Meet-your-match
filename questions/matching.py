from decimal import Decimal 
from django.contrib.auth.models import User

from . models import Question, Answer, UserAnswer, MatchAnswer


def points(request_user, matched_user):
    # prefer answer 
    pref_answers = MatchAnswer.objects.filter(user=request_user)
    actual_answers = UserAnswer.objects.filter(user=matched_user)
    total_questions = 0 
    points_awarded = 0 
    points_possible = 0 

    for ans in pref_answers:
        for act_ans in actual_answers:
            if ans.question == act_ans.question:
                total_questions += 1 
                points_possible += ans.points
                if ans.answer.answer == act_ans.answer.answer:
                    print("this is for ans.answer is :", ans.answer)
                    print("this is ans.answer.answer: ", ans.answer.answer)
                    points_awarded += ans.points
    if points_possible == 0:
        points_possible = 0.000000001
    # if id don't use Decimal it will round up or down but i want the extact one
    percentage = points_awarded/Decimal(points_possible)
    print(f"Out of {total_questions} questions, {points_awarded} points were awarded of {points_possible} points with a score of {percentage} ")
    return total_questions, percentage

def match_percentage(user_a, user_b):
    a_quests, a_percent = points(user_a, user_b)
    b_quests, b_percent = points(user_b, user_a)

    if a_quests == b_quests:
        if a_quests == 0:
            a_quests = 0.000000001
        # based on geometric mean average
        new_percent = Decimal(a_percent * b_percent)
        n = Decimal(1.0/a_quests)
        match_percent = new_percent**n
        print("This is match percent: ", match_percent)
        return match_percent
