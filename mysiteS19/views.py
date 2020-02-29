from django.http import HttpResponse, HttpResponseRedirect, HttpResponse
from django.shortcuts import render


def home(request):
    return render(request, 'Home.html')