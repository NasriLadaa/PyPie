from django.shortcuts import render, redirect, HttpResponse
from . import models
from datetime import datetime
from django.contrib import messages

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
        errors = models.User.objects.basic_validator_reg(request.POST)
        if len(errors) > 0:
            for key, value in errors.items():
                messages.error(request, value)
            print("Errors") 
            return redirect('/')    
        else:
            new_user = models.create_user(request.POST)
            request.session['user_id'] = new_user.id
            return redirect('/dashboard')
    else:
        return render(request, 'index.html')

def create_pie_form(request):
    if request.method == 'POST':
        if  'user_id' in request.session:
            errors = models.Pie.objects.basic_validator_save_Pie(request.POST)
            if len(errors) > 0:
                for key, value in errors.items():
                    messages.error(request, value)
                print("Errors") 
                return redirect('/createpie')  
            else:  
                models.create_pie(request)
                return redirect('/dashboard')
        else: 
            return redirect('/')
    else:
        return render(request, 'index.html')

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
            errors = models.Pie.objects.basic_validator_save_Pie(request.POST)
            if len(errors) > 0:
                for key, value in errors.items():
                    messages.error(request, value)
                print("Errors") 
                return redirect('/editpie/'+request.POST['pieid'])    
            else:
                models.update_pie(request.POST)
                return redirect('/dashboard')    
        else:
            return redirect('/')
    else:
        return render(request, 'index.html')    

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

# Todo : Ready
def login_user_form(request):
    if request.method == 'POST':
            errors = models.User.objects.basic_validator_login(request.POST)
            if len(errors) > 0:
                for key, value in errors.items():
                    messages.error(request, value)
                    print("Errors") 
                    return redirect('/')  
            else:
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
            'pies' : models.vote_count(),
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
    
def delete_pie_form(request):
    if request.method == 'POST':
        if  'user_id' in request.session:
            pie_id = request.POST['pieid']
            user_id = request.POST['userid']
            if request.session['user_id'] == int(user_id):
                models.delete_pie(pie_id)
                return redirect('/dashboard')
            else:
                print("test")
                return render(request, 'index.html')
        else:
            return redirect('/')
    else:
        return render(request, 'index.html')   


