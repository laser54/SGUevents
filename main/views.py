from django.shortcuts import render

def firstpage(request):
    return render(request, 'main/mainpage.html')