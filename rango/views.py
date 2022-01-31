from django.shortcuts import render
from django.http import HttpResponse 
# Import the Category model
from rango.models import Category 

#section 3.4 creating a view 
def index(request):
    #construct a dictionary to pass to the template engine as its context
    #the key boldmessage matches to {{ boldmessage }} in the template
    context_dict = {'boldmessage' : 'Crunchy, creamy, cookie, candy, cupcake!'}
    
    #return a rendered response to the client
    #first paramterer is the template we want to use 
    return render(request, 'rango/index.html', context=context_dict)

def about(request):
    context_dict = {'boldmessage' : 'This tutorial has been put together by Anya'}
    return render(request, 'rango/about.html', context=context_dict) #HttpResponse('Rango says here is the about page. <a href="/rango/">Index</a>')