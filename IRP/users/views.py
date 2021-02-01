from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout
from django.urls import reverse
from .forms import SignUpForm

# Create your views here.
def index(request):
    if not request.user.is_authenticated:
        return render(request, "users/login.html")
    context = {
        "user":request.user
    }
    return HttpResponseRedirect(reverse('home_page'))
    #return render(request, "home.html", context)

def login_view(request):
    username = request.POST['username']
    password = request.POST['password']
    #print(username)

    user = authenticate(request, username=username, password=password)
    if user is not None:
        login(request, user)
        return HttpResponseRedirect(reverse('index'))
    else:
        return render(request, "users/login.html", {"message":"Invalid credential"})

def signup_view(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            return HttpResponseRedirect(reverse('home_page'))
    else:
        form = SignUpForm()
    return render(request, 'SignUp_Login/signup.html', {'form': form})

def logout_view(request):
    logout(request)
    return render(request, "users/login.html", {'message':'Successfully loged out'})
