from django.shortcuts import render
from django.http import HttpResponse

def home(request):
    return HttpResponse("Payout Service is running")


# Create your views here.
