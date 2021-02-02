from django.core.exceptions import ValidationError
from django.shortcuts import redirect, render
from decimal import Context
from django.contrib.auth.backends import UserModel
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.urls import reverse

from datetime import datetime
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from .forms import LoginForm, SignUpForm
from django.contrib.auth import login, authenticate
from django.contrib.auth.models import User


from django.contrib.auth import get_user_model
from django.contrib.auth.models import User
from django.contrib.auth.tokens import default_token_generator
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import EmailMessage
from django.http import HttpResponse
from django.shortcuts import render
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
import re

UserModel = get_user_model()
from .forms import SignUpForm




#include models
from .models import Employee, Job, Candidate, Feedback
from .models import TestModel

#include forms
from .forms import CandidateForm, UploadJdForm
from .forms import TestForm


# Create your views here.
def index(request):
    if not request.user.is_authenticated:
        return render(request, "users/login.html")
    return HttpResponseRedirect(reverse('index'))


def add_candidate_view(request, *args, **kwargs):
    if not request.user.is_authenticated:
        return render(request, "users/login.html")
    user_id = request.session['user_id']
    user = Employee.objects.get(employee_id=user_id)
    if request.method == 'POST':
        form = CandidateForm(request.POST, request.FILES, initial={'registered_by': user})
        form.fields['registered_by'].disabled = True

        if form.is_valid():
            candidate_obj = form.save()
            requisition_id = form.cleaned_data['requisition_id']
            job_obj = Job.objects.get(requisition_id=requisition_id)
            Feedback.objects.create(
                candidate_email=candidate_obj,
                level=1,
                requisition_id=job_obj,
                status='pending',
            )
            Feedback.objects.create(
                candidate_email=candidate_obj,
                level=2,
                requisition_id=job_obj,
                status='pending',
            )
            Feedback.objects.create(
                candidate_email=candidate_obj,
                level=3,
                requisition_id=job_obj,
                status='pending',
            )
            return redirect('search_candidate')
    else:
        form = CandidateForm(initial={'registered_by': user})
        form.fields['registered_by'].disabled = True
    context = {
        'form': form
    }
    return render(request, 'add_candidate.html', context)

def upload_jd_view(request, *args, **kwargs):
    if not request.user.is_authenticated:
        return render(request, "users/login.html")
    user_id = request.session['user_id']
    user = Employee.objects.get(employee_id=user_id)
    if request.method == 'POST':
        #if someone forcefully entered raised_by_field using tampering of form
        if 'raised_by_employee' in request.POST:
            raise ValidationError('FORM IS TAMPERED')
        print(request.POST)
        form = UploadJdForm(request.POST, request.FILES, initial={'raised_by_employee':user})
        form.fields['raised_by_employee'].disabled = True
        if form.is_valid():
            print(form.cleaned_data)
            obj = form.save()
            return redirect('home_page')
    else:
        form = UploadJdForm(initial={'raised_by_employee':user})
        form.fields['raised_by_employee'].disabled = True
    context = {
        'form' : form
    }
    return render(request, 'upload_jd.html', context)

def home_view(request):
    if not request.user.is_authenticated:
        return render(request, "users/login.html")
    user_id = 101   # it is currently hardcoded but will be derived from login page itself
    request.session['user_id'] = user_id
    if request.method == 'POST':
        print(request.POST)
        if 'search_requisition_id_button' in request.POST:
            requisition_id = request.POST.get('requisition_id')
            return redirect('search_jd_page', requisition_id)
        elif 'upload_jd_button' in request.POST:
            return redirect('upload_jd_page')
        elif 'search_candidate_button' in request.POST:
            return redirect('search_candidate')
        else:
            return Http404('Page Not Exist')
    return render(request,'home.html')

def search_jd_view(request, requisition_id):
    if not request.user.is_authenticated:
        return render(request, "users/login.html")
    obj = Job.objects.get(requisition_id=requisition_id)
    if obj is not None:
        context = {
            'obj': obj
        }
        return render(request, 'jd_results.html', context)
    else:
        raise Http404("JD is not exist")

#######rudra's previous part ###############
# def search_candidate_view(request):
#     return HttpResponseRedirect(reverse("feedback", args=('python_1', 'rudra@gmail.com', 3)))

# def feedback(request, req_id, email_id, level):
#     if request.method == "POST":
#         #candidate_email = Candidate.objects.get()
#         #candidate_email = Candidate.objects.get(emailId='rudra@gmail.com')
#         #interviewer_code = Employee.objects.get(incedoCode=201201)
#         #time_stamp = datetime.timestamp(datetime.now())

#         requisition_id = 'req_id'
#         candidate_email = request.POST['candidate_email']
#         interviewer_code = request.POST['interviewer_code']
#         status = request.POST['status']
#         rating_python = request.POST['rating_python']
#         rating_java = request.POST['rating_java']
#         rating_cpp = request.POST['rating_cpp']
#         rating_sql = request.POST['rating_sql']
#         comments = request.POST['comments']

#         Feedback.objects.create(candidateEmail=Candidate.objects.get(emailId=candidate_email),
#                                 interviewerCode=Employee.objects.get(incedoCode=interviewer_code),
#                                 level=int(level)+1,
#                                 status=status,
#                                 ratingPython=rating_python,
#                                 ratingJava=rating_java,
#                                 ratingCPP=rating_cpp,
#                                 ratingSQL=rating_sql,
#                                 comments=comments,)
#         return HttpResponseRedirect(reverse('test_name'))

#     try:
#         basic_detail={'Name' :'candidate_name',
#                     'Email':email_id,
#                     'Graduation_CGPA':'candidate_cgpa',
#                     'University_name':'candidate_college_name'}

#         if(level == 1):
#              prv_feedback[level] = None

#         if(level == 2):
#             level_1 = { 'staus':'pass',
#                         'python_rating':'python_rating',
#                         'java_rating':'java_rating',
#                         'cpp_rating': 'cpp_rating',
#                         'sql_rating': 'sql_rating',
#                         'comments' : 'comments'}

#             context = {
#                 'basic_detail':basic_detail,
#                 'level_1': level_1,
#             }

#         if(level == 3):
#             level_1 = { 'staus':'pass',
#                         'python_rating':'python_rating',
#                         'java_rating':'java_rating',
#                         'cpp_rating': 'cpp_rating',
#                         'sql_rating': 'sql_rating',
#                         'comments' : 'comments'}

#             level_2 = { 'staus':'pass',
#                         'python_rating':'python_rating',
#                         'java_rating':'java_rating',
#                         'cpp_rating': 'cpp_rating',
#                         'sql_rating': 'sql_rating',
#                         'comments' : 'comments'}
#             context = {
#                 'basic_detail':basic_detail,
#                 'level_1': level_1,
#                 'level_2': level_2,
#             }

#     except Feedback.DoesNotExist:
#         raise Http404('Feedback does not exist')

#     return render(request, 'registration/feedback.html', Context)


def test_view(request, *args, **kwargs):
    if not request.user.is_authenticated:
        return render(request, "users/login.html")
    if request.method == 'POST':
        print(request.POST)
        form = TestForm(request.POST, request.FILES)
        if form.is_valid():
            obj = form.save(commit=False)
            obj = TestForm()
    else:
        form = TestForm(initial={'field1': 'initial_val'})
        form.fields['field1'].readonly = True
        print(form.fields['field1'].readonly)
        form.fields['field1'].disabled = True
    context = {
        'form' : form
    }
    return render(request, 'test.html', context)

# def signup_view(request):
#    if request.method == 'POST':
#        form = SignUpForm(request.POST)
#       if form.is_valid():
#            form.save()
#            return redirect('posts:list')
 #   else:
 #       form = SignUpForm()
  #  return render(request, 'Signup_login/signup.html', {'form': form})


# def login_view(request):
#     if request.method == 'POST':

#         form = LoginForm(data=request.POST)
#         if form.is_valid():

#             return render(request,'SignUp_Login/dashboard.html')
#     else:
#         form = LoginForm()
#     return render(request, 'Signup_Login/login.html', {'form': form})

def login_view(request):
    if request.method == 'POST':

        form = LoginForm(data=request.POST)
        if form.is_valid():

            return render(request,'SignUp_Login/dashboard.html')
    else:
        form = LoginForm()
    return render(request, 'Signup_Login/login.html', {'form': form})




#
# def login_view(request):
  #  username = request.POST['username']
 #   password = request.POST['password']
  #  print(username)

  #  user = authenticate(request, username=username, password=password)
  #  if user is not None:
   #     login(request, user)
  #      return HttpResponseRedirect(reverse('index'))
    #else:
 #       return render(request, "users/login.html", {"message":"Invalid credential"})


def signup_view(request):

    if request.method == 'POST':
        form = SignUpForm(request.POST)

        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            user.save()
            current_site = get_current_site(request)
            mail_subject = 'Activate your account.'
            message = render_to_string('accounts/acc_active_email.html', {
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': default_token_generator.make_token(user),
            })
            to_email = form.cleaned_data.get('email')
            email = EmailMessage(
                mail_subject, message, to=[to_email]
            )
            email.send()
            return HttpResponse('Please confirm your email address to complete the registration')
    else:
        form = SignUpForm()
    return render(request, 'SignUp_Login/signup.html', {'form': form})


def activate(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = UserModel._default_manager.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and default_token_generator.check_token(user, token):
        user.is_active = True
        user.save()
        return HttpResponse('Thank you for your email confirmation. Now you can login your account.')
    else:
        return HttpResponse('Activation link is invalid!')



def dashboard(request):
    return render(request, "SignUp_Login/dashboard.html")








#user = form.save()
           # username = form.cleaned_data.get('username')
           # raw_password = form.cleaned_data.get('password1')
           # user = authenticate(username=username, password=raw_password)
           # login(request, user)

           # return redirect('home')
            #else:
    #    form = SignUpForm()
   # return render(request, 'SignUp_Login/signup.html', {'form': form})


##################### RUDRA #################################
def search_candidate(request):
    if not request.user.is_authenticated:
        return render(request, "users/login.html")
    if request.method == 'POST':
        candidate_email= request.POST['search_element']
        req_id = list(set(Feedback.objects.filter(candidate_email = candidate_email).values_list('requisition_id').order_by('-requisition_id')))
        print(type(req_id))
        print(req_id)

        context = {}
        for x in range(len(req_id)):
            temp_dict={}
            print(type(req_id[x][0]))
            l1=Feedback.objects.get(requisition_id=req_id[x][0],candidate_email=candidate_email, level = 1).status

            temp_dict['req_id']=req_id[x][0];
            temp_dict['email']=candidate_email;
            if l1=='pending':
                temp_dict[1]='pending'
                temp_dict[2]='-'
                temp_dict[3]='-'
            elif l1=='fail':
                temp_dict[1]='fail'
                temp_dict[2]='NA'
                temp_dict[3]='NA'
            else :
                l2=Feedback.objects.get(requisition_id=req_id[x][0],candidate_email=candidate_email, level = 2).status
                if l2=='pending':
                    temp_dict[1]='pass'
                    temp_dict[2]='pending'
                    temp_dict[3]='-'
                elif l1=='fail':
                    temp_dict[1]='pass'
                    temp_dict[2]='fail'
                    temp_dict[3]='NA'
                else :
                    l3=Feedback.objects.get(requisition_id=req_id[x][0],candidate_email=candidate_email, level = 3).status
                    if l3=='pending':
                        temp_dict[1]='pass'
                        temp_dict[2]='pass'
                        temp_dict[3]='pending'
                    elif l3=='fail':
                        temp_dict[1]='pass'
                        temp_dict[2]='pass'
                        temp_dict[3]='fail'
                    else:
                        temp_dict[1]='pass'
                        temp_dict[2]='pass'
                        temp_dict[3]='pass'
            context[str(x)]=temp_dict



        return render(request, 'search.html',{'context':context})



    return render(request, 'search.html')

def feedback(request, req_id, email_id, level):
    if not request.user.is_authenticated:
        return render(request, "users/login.html")
    if request.method == "POST":
        interviewer_code = request.POST['interviewer_code']
        status = request.POST['status']
        rating_python = request.POST['rating_python']
        rating_java = request.POST['rating_java']
        rating_cpp = request.POST['rating_cpp']
        rating_sql = request.POST['rating_sql']
        comments = request.POST['comments']

        feedback_object = Feedback.objects.get(candidate_email=Candidate.objects.get(email=email_id), requisition_id=Job.objects.get(requisition_id = req_id), level=level, status='pending')
        feedback_object.interviewer_id = Employee.objects.get(employee_id=interviewer_code)
        feedback_object.status=status
        feedback_object.rating_python=rating_python
        feedback_object.rating_java=rating_java
        feedback_object.rating_cpp=rating_cpp
        feedback_object.rating_sql=rating_sql
        feedback_object.comments=comments
        feedback_object.save()
        '''
        Feedback.objects.create(candidate_email=Candidate.objects.get(email=email_id),
                                interviewer_id=Employee.objects.get(employee_id=interviewer_code),
                                requisition_id=Job.objects.get(requisition_id = req_id),
                                level=int(level)+1,
                                status=status,
                                rating_python=rating_python,
                                rating_java=rating_java,
                                rating_cpp=rating_cpp,
                                rating_sql=rating_sql,
                                comments=comments,)'''
        return HttpResponseRedirect(reverse('search_candidate'))

    try:
        candidate_name = Candidate.objects.get(email=email_id).full_name
        candidate_cgpa = Candidate.objects.get(email=email_id).CGPA
        candidate_college_name =  Candidate.objects.get(email=email_id).college_name
        basic_detail={'Name' :candidate_name,
                    'Email':email_id,
                    'Graduation_CGPA':candidate_cgpa,
                    'University_name':candidate_college_name}

        if(level == 1):
             context = {
                 'basic_detail':basic_detail,
                 'level':level
             }

        if(level == 2):
            status = Feedback.objects.get(candidate_email = email_id, level=level-1, requisition_id = req_id).status
            python_rating = Feedback.objects.get(candidate_email = email_id, level=level-1, requisition_id = req_id).rating_python
            java_rating = Feedback.objects.get(candidate_email = email_id, level=level-1, requisition_id = req_id).rating_java
            cpp_rating = Feedback.objects.get(candidate_email = email_id, level=level-1, requisition_id = req_id).rating_cpp
            sql_rating = Feedback.objects.get(candidate_email = email_id, level=level-1, requisition_id = req_id).rating_sql
            comments = Feedback.objects.get(candidate_email = email_id, level=level-1, requisition_id = req_id).comments
            level_1 = { 'status': status,
                        'python_rating': python_rating,
                        'java_rating': java_rating,
                        'cpp_rating': cpp_rating,
                        'sql_rating': sql_rating,
                        'comments' : comments}

            context = {
                'basic_detail':basic_detail,
                'level_1': level_1,
                'level':level
            }

        if(level == 3):
            status = Feedback.objects.get(candidate_email = email_id, level=level-2, requisition_id = req_id).status
            python_rating = Feedback.objects.get(candidate_email = email_id, level=level-2, requisition_id = req_id).rating_python
            java_rating = Feedback.objects.get(candidate_email = email_id, level=level-2, requisition_id = req_id).rating_java
            cpp_rating = Feedback.objects.get(candidate_email = email_id, level=level-2, requisition_id = req_id).rating_cpp
            sql_rating = Feedback.objects.get(candidate_email = email_id, level=level-2, requisition_id = req_id).rating_sql
            comments = Feedback.objects.get(candidate_email = email_id, level=level-2, requisition_id = req_id).comments

            status_ = Feedback.objects.get(candidate_email = email_id, level=level-1, requisition_id = req_id).status
            python_rating_ = Feedback.objects.get(candidate_email = email_id, level=level-1, requisition_id = req_id).rating_python
            java_rating_ = Feedback.objects.get(candidate_email = email_id, level=level-1, requisition_id = req_id).rating_java
            cpp_rating_ = Feedback.objects.get(candidate_email = email_id, level=level-1, requisition_id = req_id).rating_cpp
            sql_rating_ = Feedback.objects.get(candidate_email = email_id, level=level-1, requisition_id = req_id).rating_sql
            comments_ = Feedback.objects.get(candidate_email = email_id, level=level-1, requisition_id = req_id).comments
            level_1 = { 'status': status,
                        'python_rating': python_rating,
                        'java_rating': java_rating,
                        'cpp_rating': cpp_rating,
                        'sql_rating': sql_rating,
                        'comments' : comments}

            level_2 = { 'status': status_,
                        'python_rating': python_rating_,
                        'java_rating': java_rating_,
                        'cpp_rating': cpp_rating_,
                        'sql_rating': sql_rating_,
                        'comments' : comments_}
            context = {
                'basic_detail':basic_detail,
                'level_1': level_1,
                'level_2': level_2,
                'level': level,
            }

    except Feedback.DoesNotExist:
        raise Http404('Feedback does not exist')

    return render(request, 'registration/feedback.html', context)

def edit(request, req_id, email_id, level):
    if not request.user.is_authenticated:
        return render(request, "users/login.html")

    if request.method == 'POST':
        obj_ = Feedback.objects.get(candidate_email=email_id, requisition_id=req_id, level=level)
        obj_.interviewer_id = Employee.objects.get(employee_id=request.POST['interviewer_id'])
        obj_.status = request.POST['status']
        obj_.rating_python = request.POST['rating_python']
        obj_.rating_java = request.POST['rating_java']
        obj_.rating_cpp = request.POST['rating_cpp']
        obj_.rating_sql = request.POST['rating_sql']
        obj_.comments = request.POST['comments']
        obj_.save()

        return HttpResponseRedirect(reverse('search_candidate'))

    try:
        obj= Feedback.objects.get(candidate_email=email_id, requisition_id=req_id, level=level)
        Context = vars(obj)
        return render(request, 'registration/edit.html', Context)
    except:
        return HttpResponse('No details Found')


def test(request):
    if not request.user.is_authenticated:
        return render(request, "users/login.html")

    return HttpResponse('inside the test')
