from django.shortcuts import render, redirect, HttpResponse
from . import models

def index(request):
    return render(request , 'index.html')


def display_dashboard(request):
    context = {
        'users' , models.get_users()
    }
    return render(request, 'dashboard', context)

