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
        return render(request, 'index.html')

def create_pie_form(request):
    if request.method == 'POST':
        if  'user_id' in request.session:
            models.create_pie(request)
            return redirect('/dashboard')
        else:
            return redirect('/')
    else:
        return render(request, 'dashboard.html')

def update_pie(request, id):
    if 'user_id' in request.session:
        context = {
            'pie' : models.get_pie(id),
            'current_year': datetime.now().year
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
        user_id = request.session['user_id'] 
        context = {
            'pie' : models.get_pie(id),
            'is_vote' : models.check_vote(user_id , id),
            'current_year': datetime.now().year
        }
        return render(request, 'showpie.html' ,context)
    else:
        return redirect('/')

# Todo : still under implementation 
def login_user_form(request):
    if request.method == 'POST':
        user = models.login_user(request)
        if (user):
            return redirect('/dashboard')
        else:
            return render(request, 'index.html')
    else:
        return render(request, 'index.html')     #it should be error page
    
def vote_pie_form(request):
    if request.method == 'POST':
        if  'user_id' in request.session:
            user_id = request.session['user_id']
            pie_id = request.POST['pie_id']
            form_type = request.POST['form_type']
            if ( form_type == 'yakee'):
                models.unvote_pie( user_id ,  pie_id)
                return redirect('/viewpie/'+pie_id)
            else: #Delicious
                models.vote_pie( user_id ,  pie_id)
                return redirect('/viewpie/'+pie_id)
        else:
            return redirect('/')
    else:
        context = {
        'current_year': datetime.now().year
        }
        return render(request, 'dashboard.html', context)   #it should be error page
    
def show_votes(request):
    if 'user_id' in request.session:
        context = {
            'current_year': datetime.now().year
        }
        return render(request, 'votes.html' ,context)
    else:
        return redirect('/')    
    
def view_user(request):
    if 'user_id' in request.session:
        context = {
            'user' : models.get_user(request.session['user_id']),
            'current_year': datetime.now().year
        }
        return render(request, 'viewuser.html' ,context)
    else:
        return redirect('/')        