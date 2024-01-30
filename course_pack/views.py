from django.contrib import messages
from django.contrib.messages import constants
from django.http import HttpResponse
from django.shortcuts import render, redirect
from course_pack.models import CoursePack, ViewCoursePack


def add_course_pack(request):
    if request.method == 'GET':
        course_packs = CoursePack.objects.filter(user=request.user)
        total_views = ViewCoursePack.objects.filter(course_pack__user=request.user).count()
        return render(request,
                      'add_course_pack.html',
                      {'course_packs': course_packs, 'total_views': total_views})

    elif request.method == 'POST':
        title = request.POST.get('title')
        file = request.FILES.get('file')

        course_pack = CoursePack(
            user=request.user, title=title, file=file
        )

        course_pack.save()
        messages.add_message(request, constants.SUCCESS, 'Successfully added')
        return redirect('/course_pack/add_course_pack')


def course_pack(request, id):
    course_pack = CoursePack.objects.get(id=id)
    total_views = ViewCoursePack.objects.filter(course_pack=course_pack).count()
    single_views = ViewCoursePack.objects.filter(course_pack=course_pack).values('ip').distinct().count()

    view = ViewCoursePack(
        ip=request.META.get('REMOTE_ADDR'),
        course_pack=course_pack
    )
    view.save()
    return render(request,
                  'course_pack.html',
                  {'course_pack': course_pack, 'total_views': total_views, 'single_views': single_views})
