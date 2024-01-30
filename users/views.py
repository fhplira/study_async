from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.messages import constants
from django.contrib import messages
from django.contrib import auth


def register(request):
    if request.method == 'GET':
        return render(request, 'register.html')
    elif request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']

        if not password == confirm_password:
            messages.add_message(request, constants.ERROR, 'Passwords are not the same')
            return redirect('/users/register')

        user = User.objects.filter(username=username)
        if user.exists():
            messages.add_message(request, constants.ERROR, 'User already exists')
            return redirect('/users/register')

        try:
            User.objects.create_user(
                username=username,
                password=password

            )
            messages.add_message(
                request, constants.SUCCESS, 'User created successfully'
            )

            return redirect('/users/log_in')
        except:
            messages.add_message(request, constants.ERROR, 'An error occurred')
            return redirect('/users/register')


def log_in(request):
    if request.method == 'GET':
        return render(request, 'login.html')

    elif request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = auth.authenticate(request, username=username, password=password)

        if user is not None:
            auth.login(request, user)
            messages.add_message(request, constants.SUCCESS, 'Logged in successfully')
            return redirect('/flashcard/new_flashcard')

        else:
            messages.add_message(request, constants.ERROR, 'Invalid login details')
            return redirect('/users/log_in')


def logout(request):
    auth.logout(request)
    return redirect('/users/log_in')

