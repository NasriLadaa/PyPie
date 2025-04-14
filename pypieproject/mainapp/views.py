from django.shortcuts import render, redirect, HttpResponse
from . import models

def index(request):
    return render(request , 'index.html')


def display_dashboard(request):
    if 'user_id' in request.session:
        context = {
            'users' : models.get_users()
        }
        return render(request, 'dashboard.html', context)
    else:
        return redirect('/')

def create_pie(request):
    if 'user_id' in request.session:
        return render(request, 'createpie.html')
    else:
        return redirect('/')

def create_user_form(request):
    if request.method == 'POST':
        new_user = models.create_user(request.POST)
        request.session['user_id'] = new_user.id
        return redirect('/dashboard')
    else:
        return render(request, 'dashboard.html')


def create_pie_form(request):
    if request.method == 'POST':
        if  'id' in request.session:
            #create bie to ORM
            return redirect('/dashboard')
        else:
            return redirect('/')
    else:
        return render(request, 'dashboard.html')

def update_pie(request):
    if 'id' in request.session:
        return render(request, 'updatepie.html')
    else:
        return redirect('/')

def update_pie_form(request):
    return redirect('/dashboard')


def logout_form(request):
    if 'id' in request.session:
        del request.session['user_id']
        return redirect('/')
    else:
        return redirect('/')