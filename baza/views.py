from django.shortcuts import render, get_object_or_404, redirect
from .models import Quiz, Question, Answer, UserResponse

def quiz_list(request):
    quizzes = Quiz.objects.all()
    return render(request, 'quiz/quiz_list.html', {'quizzes': quizzes})

def quiz_detail(request, quiz_id):
    quiz = get_object_or_404(Quiz, id=quiz_id)
    questions = quiz.question_set.all()
    return render(request, 'quiz/quiz_detail.html', {'quiz': quiz, 'questions': questions})

def submit_quiz(request, quiz_id):
    if request.method == 'POST':
        quiz = get_object_or_404(Quiz, id=quiz_id)
        score = 0
        for question in quiz.question_set.all():
            answer_id = request.POST.get(f'question_{question.id}')
            if answer_id:
                answer = get_object_or_404(Answer, id=answer_id)
                UserResponse.objects.create(
                    user=request.user.username,
                    question=question,
                    answer=answer
                )
                if answer.is_correct:
                    score += 1
        return render(request, 'quiz/quiz_result.html', {'score': score, 'total': quiz.question_set.count()})
    return redirect('quiz_detail', quiz_id=quiz_id)