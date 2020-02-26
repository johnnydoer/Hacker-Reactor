from django.shortcuts import render, redirect
from .models import User
from django.core.mail import send_mail
from django.shortcuts import HttpResponse
from .forms import RegisterForm, LoginForm, ResetForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from django.core.mail import EmailMessage
from .tokens import account_activation_token
from .forms import ResetPasswordForm
# from dashboard.models import course_dashboard
# from .models import course
# from .serailizer import courselogserializer
# from rest_framework.response import Response
# from rest_framework.decorators import api_view


# login

def login_display(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            emailid = form.cleaned_data.get("emailid")
            password = form.cleaned_data.get('password')
            print(emailid)
            userlog = User.objects.get(email=emailid)
            print(userlog)
            user = authenticate(username=userlog, password=password)
            if user:
                if user.is_active:
                    login(request, user)
                    return redirect('Main:index')
                else:
                    return HttpResponse('Not registered')
    else:
        form = LoginForm()
    context = {
        'form': form
    }
    return render(request, 'Main/login.html', context)


# register
def register_display(request):
    if request.user.is_authenticated:
        return render(request, 'Main/index.html')
    if request.method == 'POST':
        form = RegisterForm(request.POST or None)
        # print("***********", request, "*************")
        if form.is_valid():
            user = User.objects.create_user(username=form.cleaned_data["username"],
                                            email=form.cleaned_data["email"],
                                            password=form.cleaned_data["password"]
                                            )

            user.first_name = form.cleaned_data["first_name"]
            user.last_name = form.cleaned_data["last_name"]
            user.birth_date = form.cleaned_data["birth_date"]
            user.is_active = False
            user.save()
            mail = form.cleaned_data.get('email')
            print(mail)
            current_site = get_current_site(request)
            mail_subject = 'Activate your account.'
            message = render_to_string('Main/acc_active_email.html', {
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': account_activation_token.make_token(user),
            })
            to_email = form.cleaned_data.get('email')
            email = EmailMessage(
                mail_subject, message, to=[to_email]
            )
            email.send()
            # send_mail(mail_subject, message, 'iiits2021@gmail.com', [mail])
            return render(request, 'Main/email_confirmation.html')

    else:
        form = RegisterForm()
    context = {
        'form': form,
    }
    return render(request, 'Main/register1.html', context)


'''
logout
'''


@login_required
def logout_view(request):
    logout(request)
    return redirect('Main:login')


'''
forgot password
'''


def reset_password(request):
    if request.method == 'POST':
        form1 = ResetForm(request.POST)
        if form1.is_valid():
            mail = form1.cleaned_data.get('email')
            user = User.objects.get(email=mail)
            current_site = get_current_site(request)
            mail_subject = 'Password Reset Link.'
            message = render_to_string('Main/reset_confirm_email.html', {
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': account_activation_token.make_token(user),
            })

            send_mail(mail_subject, message, 'iiits2021@gmail.com', [mail])
            return render(request, 'Main/reset_email.html', {'form': form1, 'message': 'Email has been sent to  ' + mail})
    else:
        form1 = ResetForm()
    return render(request, 'Main/reset_email.html', {'form': form1, 'message': ''})


def display_reset_password(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        print(uid)
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        # login(request, user)
        request.session['email'] = user.email
        return redirect('Main:save_password')

    else:
        return HttpResponse('Activation link is invalid!')


def save_password(request):
    if request.method == "POST":
        form1 = ResetPasswordForm(request.POST)
        if form1.is_valid():
            mail = request.session['email']
            user = User.objects.get(email=mail)
            print(user)
            user.set_password(form1.cleaned_data.get('new_password'))
            user.save()
            return HttpResponse(
                "Password has been reset Please login<a href='{{ url 'registrartion:login' }}'>here</a>")
    else:
        form1 = ResetPasswordForm()
    return render(request, 'Main/reset_password.html', {'form': form1})


def activate(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        print(uid)
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        login(request, user)
        return redirect('Main:index')

    else:
        return HttpResponse('Activation link is invalid!')


def index(request):
    return render(request, "Main/index.html", {'data':request.user.is_authenticated})