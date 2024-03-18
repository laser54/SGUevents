from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect

def log_in(request):
    return render(request, 'users/users_log_in.html')

def sign_up(request):
    return render(request, 'users/users_sign_up.html')
