from django.shortcuts import render, redirect
from django.contrib import messages
from .models import *

# Create your views here.

def index(request):
    context = {
        "courses": Course.objects.all()
        }
    return render(request, 'home.html', context)

def create(request):
    errors = Course.objects.validator(request.POST)
    if len(errors):
        for key, value in errors.items():
            messages.error(request, value)
    else:
        course = Course.objects.create(
            name = request.POST['course_name']
        )
        description = Description.objects.create(
            content=request.POST['description']
        )
        course.description = description
        course.save()
        
    return redirect('/courses')

def delete(request, id):
    if request.method == "GET":
        context = {
            "course": Course.objects.get(id=id)
        }
        return render(request,'delete.html', context)

    if request.method == "POST":
        course = Course.objects.get(id=id)
        course.delete()
        return redirect('/courses')

def comments(request, id):
    context = {
        "course": Course.objects.get(id=id)
    }
    return render(request,'comments.html', context)

def create_comment(request, id):
    errors = Comment.objects.validator(request.POST)
    if len(errors):
        for key, value in errors.items():
            messages.error(request, value)
    else:
        Comment.objects.create(
            content=request.POST['content'],
            course = Course.objects.get(id=id)
        )
    return redirect(f'/courses/{id}')