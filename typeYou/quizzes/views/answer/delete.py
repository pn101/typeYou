from django.conf import settings
from django.contrib import messages
from django.core.urlresolvers import reverse
from django.shortcuts import redirect
from django.views.generic import View

from quizzes.models import Question, Quiz, Solve


class AnswerDeleteView(View):

    def get(self, request, *args, **kwargs):

        hash_id = self.kwargs.get('slug')
        quiz = Quiz.objects.public().get(hash_id=hash_id)

        if request.user == quiz.user:
            return redirect(reverse("home"))

        if quiz not in request.user.solve_quiz_set.public():  # if submitted answer does not exist
            messages.add_message(
                request,
                messages.ERROR,
                settings.ANSWER_DOES_NOT_EXIST_ERROR_MESSAGE,
            )
            return redirect(reverse("quizzes:quiz_detail", kwargs={
                'slug': hash_id,
                })
            )

        answers = quiz.answer_set.public().filter(user=request.user)

        for answer in answers:
            answer.is_public = False
            answer.save()

        solved_quiz = Solve.objects.get(user=request.user, quiz=quiz)
        solved_quiz.delete()

        messages.add_message(
            request,
            messages.SUCCESS,
            settings.ANSWER_DELETE_SUCCESS_MESSAGE,
        )
        return redirect(reverse("quizzes:quiz_detail", kwargs={
            'slug': hash_id,
            })
        )
