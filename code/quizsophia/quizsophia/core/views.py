from django.shortcuts import render
from django.http import HttpResponse
from .forms import ContactCourse

def home(request):
    return render(request, 'home.html')
