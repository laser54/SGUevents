from django.shortcuts import render

def index(request):
	return render(request, 'application_for_admin_rights/index.html')