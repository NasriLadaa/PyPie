from django.shortcuts import render, redirect, HttpResponse
from . import models
from datetime import datetime

def index(request):
    context = {
    'current_year': datetime.now().year
    }
    return render(request , 'index.html',context)

def display_dashboard(request):
    if 'user_id' in request.session:
        context = {
            'pies' : models.get_pies(),
            'current_year': datetime.now().year
        }
        return render(request, 'dashboard.html', context)
    else:
        return redirect('/')

def create_pie(request):
    if 'user_id' in request.session:
        context = {
        'current_year': datetime.now().year
        }
        return render(request, 'createpie.html', context)
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
        if  'user_id' in request.session:
            models.create_pie(request.POST)
            return redirect('/dashboard')
        else:
            return redirect('/')
    else:
        return render(request, 'dashboard.html')

def update_pie(request, id):
    if 'user_id' in request.session:
        context = {
            'pie' : models.get_pie(id)
        }
        return render(request, 'updatepie.html' ,context)
    else:
        return redirect('/')

def update_pie_form(request):
    if request.method == 'POST':
        if  'user_id' in request.session:
            models.update_pie(request.POST)
            return redirect('/dashboard')
        else:
            return redirect('/')
    else:
        return render(request, 'dashboard.html')    

def logout_form(request):
    if 'user_id' in request.session:
        del request.session['user_id']
        return redirect('/')
    else:
        return redirect('/')
    
def view_pie(request, id):
    if 'user_id' in request.session:
        context = {
            'pie' : models.get_pie(id)
        }
        return render(request, 'showpie.html' ,context)
    else:
        return redirect('/')
    
def login_user_form(request):
    if request.method == 'POST':
        #bcrypt
        request.session['user_id'] = 1
        return redirect('/dashboard')
    else:
        return render(request, 'dashboard.html')   #it should be error page