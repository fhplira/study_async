from django.contrib import messages
from django.contrib.messages import constants
from django.http import HttpResponse, Http404
from django.shortcuts import render, redirect
from .models import Category, Flashcard, Challenge, FlashcardChallenge


def new_flashcard(request):
    if not request.user.is_authenticated:
        return redirect('/users/log_in')

    if request.method == 'GET':
        categories = Category.objects.all()
        difficulties = Flashcard.DIFFICULTY_CHOICES
        flashcards = Flashcard.objects.filter(user=request.user)

        category_filter = request.GET.get('category')
        difficulty_filter = request.GET.get('difficulty')

        if category_filter:
            flashcards = flashcards.filter(category__id=category_filter)
        if difficulty_filter:
            flashcards = flashcards.filter(difficulty=difficulty_filter)

        return render(
            request,
            'new_flashcard.html',
            {'categories': categories, 'difficulties': difficulties, 'flashcards': flashcards}
        )

    elif request.method == 'POST':
        question = request.POST['question']
        answer = request.POST['answer']
        category = request.POST.get('category')
        difficulty = request.POST.get('difficulty')

        if len(question.strip()) == 0 or len(answer.strip()) == 0:
            messages.add_message(
                request,
                constants.ERROR,
                'Fill all fields',
            )
            return redirect('/flashcard/new_flashcard')

        flashcard = Flashcard(
            user=request.user,
            question=question,
            answer=answer,
            category_id=category,
            difficulty=difficulty,
        )

        flashcard.save()

        messages.add_message(
            request, constants.SUCCESS, 'Flashcard created successfully!'
        )
        return redirect('/flashcard/new_flashcard')


def delete_flashcard(request, id):
    flashcard = Flashcard.objects.filter(user=request.user).get(id=id)
    flashcard.delete()
    messages.add_message(
        request, constants.SUCCESS, 'Flashcard deleted successfully!'
    )

    return redirect('/flashcard/new_flashcard/')


def init_challenge(request):
    if request.method == 'GET':
        categories = Category.objects.all()
        difficulties = Flashcard.DIFFICULTY_CHOICES
        return render(
            request,
            'init_challenge.html',
            {'categories': categories, 'difficulties': difficulties},
        )

    elif request.method == 'POST':
        title = request.POST.get('title')
        categories = request.POST.getlist('category')
        difficulties = request.POST.get('difficulty')
        amount_questions = request.POST.get('amount_questions')

        challenge = Challenge(
            user=request.user,
            title=title,
            amount_questions=amount_questions,
            difficulty=difficulties,
        )
        challenge.save()
        challenge.category.add(*categories)

        flashcard = (
            Flashcard.objects.filter(user=request.user)
            .filter(difficulty=difficulties)
            .filter(category_id__in=categories)
            .order_by('?')
        )

        if flashcard.count() < int(amount_questions):
            return redirect('/flashcard/init_challenge/')

        flashcards = flashcard[: int(amount_questions)]

        for f in flashcards:
            flashcard_challenge = FlashcardChallenge(
                flashcard=f,
            )
            flashcard_challenge.save()
            challenge.flashcards.add(flashcard_challenge)

            challenge.save()

        return redirect(f'/flashcard/challenge/{challenge.id}')


def list_challenge(request):
    challenges = Challenge.objects.filter(user=request.user)
    # Desenvolver a parte de status
    # E a parte dos filtros
    return render(request, 'list_challenge.html', {'challenges': challenges})


def challenge(request, id):
    challenge = Challenge.objects.get(id=id)
    if not challenge.user == request.user:
        raise Http404()
    if request.method == 'GET':
        hits = challenge.flashcards.filter(answered=True).filter(got_it_right=True).count()
        misses = challenge.flashcards.filter(answered=True).filter(got_it_right=False).count()
        not_answered = challenge.flashcards.filter(answered=False).count()
        return render(
            request,
            'challenge.html',
            {
                'challenge': challenge, 'hits': hits, 'misses': misses, 'not_answered': not_answered
            },
        )


def answer_flashcard(request, id):
    flashcard_challenge = FlashcardChallenge.objects.get(id=id)
    got_it_right = request.GET.get('got_it_right')
    challenge_id = request.GET.get('challenge_id')

    flashcard_challenge.answered = True
    flashcard_challenge.got_it_right = True if got_it_right == "1" else False
    flashcard_challenge.save()

    if not flashcard_challenge.flashcard.user == request.user:
        raise Http404()

    return redirect(f'/flashcard/challenge/{challenge_id}')


def report(request, id):
    challenge = Challenge.objects.get(id=id)
    hits = challenge.flashcards.filter(answered=True).filter(got_it_right=True).count()
    misses = challenge.flashcards.filter(answered=True).filter(got_it_right=False).count()
    answered = challenge.flashcards.filter(answered=True).count()

    if answered > 0:
        data_report = [hits, misses]
    else:
        data_report = [0, 0]

    categories = challenge.category.all()
    names_category = [i.name for i in categories]

    categories_report = []
    for category in categories:
        categories_report.append(challenge.flashcards.
                                 filter(flashcard__category=category).
                                 filter(got_it_right=True).count())

    return render(
        request,
        'report.html',
        {'challenge': challenge, 'data_report': data_report,
         'names_category': names_category, 'categories_report': categories_report}
    )
