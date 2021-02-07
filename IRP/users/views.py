from django import forms
from django.shortcuts import redirect, render
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout
from django.urls import reverse
from django.urls.base import reverse_lazy
from .forms import SignUpForm

from django.contrib.auth.models import User

from django.contrib.auth.forms import AuthenticationForm, UserCreationForm, PasswordChangeForm
from .forms import LoginForm, SignUpForm
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.models import User
from django.contrib.auth.views import PasswordChangeDoneView, PasswordChangeView

from django.contrib.auth import get_user_model
from django.contrib.auth.models import User
from django.contrib.auth.tokens import default_token_generator
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import EmailMessage, message
from django.http import HttpResponse
from django.shortcuts import render
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
import re
from django.contrib import messages

UserModel = get_user_model()
from .forms import SignUpForm


 

from Incedoinc.models import Employee




def signup_view(request):

    if request.method == 'POST':
        form = SignUpForm(request.POST)

        if form.is_valid():
            
            user = form.save(commit=False)
            user.is_active = False
            user.save()
            current_site = get_current_site(request)
            mail_subject = 'Activate your IRP account.'
            message = render_to_string('accounts/acc_active_email.html', {
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': default_token_generator.make_token(user),
            })
            to_email = form.cleaned_data.get('username')
            email = EmailMessage(
                mail_subject, message, to=[to_email]
            )
            email.send()

            ###### creating employee ######
            Employee.objects.create(
                full_name = request.POST['name'],
                email = request.POST['username'],
                employee_id = request.POST['employee_id'],
            )
            return HttpResponse('<h2 >Please click the link sent to your email to complete the registration.</h2>')
    else:
        form = SignUpForm()
    return render(request, 'SignUp_Login/signup.html', {'form': form})


def activate(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = UserModel._default_manager.get(pk=uid) #Giving Error
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and default_token_generator.check_token(user, token):
        user.is_active = True
        user.save()
        form = LoginForm(data=request.POST)
        # return render(request, 'Signup_Login/login.html', {'form': form})
        return redirect('login')
    else:
        return HttpResponse('<h1>Activation link is invalid!</h1>')




def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request=request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
               #messages.info(request, f"You are now logged in as {username}")
                return redirect('home_page')
            else:
                messages.error(request, "Invalid username or password.")
        else:
            messages.error(request, "Invalid username or password.")
    form = LoginForm()
    return render(request = request,
                    template_name = "SignUp_Login/login.html",
                    context={"form":form})


def logout_view(request):
    if not request.user.is_authenticated:
        return redirect('login')
    logout(request)
    # form = SignUpForm(request.POST)
    return redirect('login')
    
class change_password_view(PasswordChangeView):
    
    form_class = PasswordChangeForm
    success_url = reverse_lazy('password_success')

def password_success(request):
    if not request.user.is_authenticated:
        return redirect('login')
    return render(request, 'accounts/password_change_done.html', {})


# def change_password_view(request):
#     if(request.method == 'GET'):
#         return render(request, 'accounts/change_password_page.html') 










			

		




   





















































# # Create your views here.
# # def index(request):
# #     if not request.user.is_authenticated:
# #         return render(request, "users/login.html")
# #     context = {
# #         "user":request.user
# #     }
# #     return HttpResponseRedirect(reverse('home_page'))
# #     return render(request, "home.html", context)


# def index(request):
#     return HTTPResponse('Vaishnavi\'s Page')

# def login_view(request):
#     username = request.POST['username']
#     password = request.POST['password']
#     #print(username)

#     user = authenticate(request, username=username, password=password)
#     if user is not None:
#         login(request, user)
#         return HttpResponseRedirect(reverse('index'))
#     else:
#         return render(request, "users/login.html", {"message":"Invalid credential"})

# def signup_view(request):
#     if request.method == 'POST':
#         form = SignUpForm(request.POST)
#         if form.is_valid():
#             user_ = User.objects.create_user(username=str(form.cleaned_data['email']), password=form.cleaned_data['password'])
#             print(user_.username)
#             user_.save()
#             user = form.save()

#             return HttpResponseRedirect(reverse('home_page'))
#     else:
#         form = SignUpForm()
#     return render(request, 'SignUp_Login/signup.html', {'form': form})

# def logout_view(request):
#     logout(request)
#     return render(request, "users/login.html", {'message':'Successfully loged out'})
