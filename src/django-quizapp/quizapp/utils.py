from decimal import Decimal


def grade_quiz(player_answers):
    ''' Grades player_answers and returns a score iff all questions are multiple choice. '''

    number_of_correct_answers = 0
    for player_answer in player_answers:
        question = player_answer.question
        if not question.is_multiple_choice():
            return None

        correct_letter = question.multiple_choice_answer
        if correct_letter == player_answer.multiple_choice_answer:
            number_of_correct_answers += 1

    grade = float(number_of_correct_answers)/float(len(player_answers)) * 100
    grade = Decimal(grade)

    return grade