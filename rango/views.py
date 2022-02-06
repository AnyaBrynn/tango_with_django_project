from django.shortcuts import render
from django.http import HttpResponse 
from rango.models import Category, Page 
from rango.forms import CategoryForm, PageForm, UserForm, UserProfileForm 
from django.shortcuts import redirect
from django.urls import reverse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

#section 3.4 creating a view 
def index(request):
   
    category_list = Category.objects.order_by('-likes')[:5]
    page_list = Page.objects.order_by('-views')[:5]
    
    context_dict = {}
    context_dict['boldmessage'] = 'Crunchy, creamy, cookie, candy, cupcake!'
    context_dict['categories'] = category_list 
    context_dict['pages'] = page_list
    
    # Render the response and send it back! 
    return render(request, 'rango/index.html', context=context_dict)
    

def about(request):
    context_dict = {'boldmessage' : 'This tutorial has been put together by Anya'}
    return render(request, 'rango/about.html', context=context_dict) #HttpResponse('Rango says here is the about page. <a href="/rango/">Index</a>')

def show_category(request, category_name_slug):
    # Create a context dictionary to pass to the template rendering engine
    context_dict = {}
    
    try: 
        # If we can't, the .get() method raises a DoesNotExist exception.
        # The .get() method returns one model instance or raises an exception. 
        category = Category.objects.get(slug=category_name_slug)
        
        # Retrieve all of the associated pages.
        # filter() returns a list of page objects or an empty list.
        pages = Page.objects.filter(category=category)
        
        # Adds our results list to the template context under name pages 
        context_dict['pages'] = pages
      
        # We also add the category object from the database to the context dict
        # We'll use this in the template to verify that the category exists. 
        context_dict['category'] = category 
    except Category.DoesNotExist:
        # We get here if we ddn't fine the specified categoy.
        # Don't do anything - the template will display the "no category" message 
        context_dict['category'] = None
        context_dict['pages'] = None 
        
    # Go render the response and return it to the client 
    return render(request, 'rango/category.html', context=context_dict)

@login_required
def add_category(request):
    form = CategoryForm()
    
    if request.method == 'POST':
        form = CategoryForm(request.POST)
        
        if form.is_valid():
            # save new category to the database
            form.save(commit=True)
            # now that category is saved, confirm it, redirect user back to index view 
            return redirect(reverse('rango:index'))
        else:
            print(form.errors)
    return render(request, 'rango/add_category.html', {'form': form})

@login_required
def add_page(request, category_name_slug):
    try:
        category = Category.objects.get(slug=category_name_slug)
    except Category.DoesNotExist:
        category = None
        
    if category is None:
        return redirect(reverse('rango:index'))
    
    form = PageForm()
    
    if request.method == 'POST':
        form = PageForm(request.POST)
        
        if form.is_valid():
            if category:
                page = form.save(commit=False)
                page.category = category
                page.views = 0
                page.save()
                
                return redirect(reverse('rango:show_category', 
                                        kwargs={'category_name_slug':
                                                category_name_slug}))
            else:
                print(form.errors)
                
    context_dict = {'form': form, 'category': category}
    return render(request, 'rango/add_page.html', context=context_dict)

def register(request):
    
    registered = False
    
    if request.method == 'POST': 
        user_form = UserForm(request.POST)
        profile_form = UserProfileForm(request.POST)
        
        if user_form.is_valid() and profile_form.is_valid():
            # saves user's form to the database 
            user = user_form.save() 
            
            # hash the password, then update the user object
            user.set_password(user.password)
            user.save()
            
            # sort out the UserProfile instance
            # commit=False delats saving model -> avoids integrity problems 
            profile = profile_form.save(commit=False)
            profile.user = user 
            
            # if the user has a profile picture 
            if 'picture' in request.FILES:
                profile.picture = request.FILES['picture']
            
            profile.save()
            registered = True
        else:
            print(user_form.errors, profile_form.errors)
    else:
        # if not HTTP POST, render using ModelForm instances 
        user_form = UserForm()
        profile_form = UserProfileForm()
    
    return render(request, 
                  'rango/register.html',
                  context = {'user_form': user_form, 
                             'profile_form': profile_form,
                             'registered': registered})

def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(username=username, password=password)

        if user:
            if user.is_active:
                login(request, user)
                return redirect(reverse('rango:index'))
            else:
                return HttpResponse("Your Rango account is disabled.")
        else:
            print(f"Invalid login details: {username}, {password}")
            return HttpResponse("Invalid login details supplied.")
    else:
        return render(request, 'rango/login.html')

@login_required
def restricted(request):
    return render(request, 'rango/restricted.html')

@login_required
def user_logout(request):
    logout(request)
    return redirect(reverse('rango:index'))