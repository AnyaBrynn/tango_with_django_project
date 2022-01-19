from django.shortcuts import render

#section 3.4 creating a view 
from django.http import HttpResponse 
def index(request):
    return HttpResponse("Rango says hey there partner!")