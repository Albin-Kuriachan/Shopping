import uuid
import time

from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from .models import CustomUser
from django.contrib import messages, auth
from .forms import *

# def signup(request):
#     if request.method == 'POST':
#         form = RegisterForm(request.POST)
#         if form.is_valid():
#             form.save()
#             return redirect(signin)
#     else:
#         form = RegisterForm()
#     return render(request, 'signup.html', {'form': form})


import random
from django.core.mail import send_mail

# Assuming you have a model named OTPRecord to store OTPs
from .send_otp import send_otp_email, send_forget_password_mail

import random
from django.shortcuts import render, redirect
from .forms import RegisterForm
import random
from django.shortcuts import render, redirect
from .forms import RegisterForm

def signup(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)

        if form.is_valid():
            otp = ''.join([str(random.randint(0, 9)) for _ in range(4)])
            print(otp)
            send_otp_email(form.cleaned_data['email'], otp)
            request.session['otp'] = otp
            request.session['email'] = form.cleaned_data['email']
            request.session['password'] = form.cleaned_data['password1']
            request.session['first_name'] = form.cleaned_data['first_name']
            request.session['last_name'] = form.cleaned_data['last_name']
            messages.success(request, 'Enter OTP  verify your email.')
            # verify_otp(request)
            return redirect('verify_otp')

    else:
        form = RegisterForm()
    return render(request, 'signup.html', {'form': form})

def verify_otp(request):
    otp = request.session.get('otp')
    if otp is None:
        return redirect(signup)
    if request.method == 'POST':
        otp_entered = request.POST.get('otp')
        if otp == otp_entered:
            form_data = {
                'email': request.session.get('email'),
                'password1': request.session.get('password'),
                'password2': request.session.get('password'),
                'first_name': request.session.get('first_name'),
                'last_name': request.session.get('last_name')
            }
            form = RegisterForm(form_data)
            if form.is_valid():
                form.save()
                del request.session['otp']
                del request.session['email']
                del request.session['password']
                del request.session['first_name']
                del request.session['last_name']
                messages.success(request, 'Registration completed Login Now  .')
                return redirect('signin')
            else:
                return render(request, 'verify_otp.html', {'error_message': 'Invalid Form Data'})
        else:
            messages.danger(request, 'Invalid OTP ')
            return render(request, 'verify_otp.html', {'error_message': 'Invalid OTP'})

    else:
        email = request.session.get('email')
        return render(request, 'verify_otp.html', {'email': email})


def signin(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']

            print(email, password)
            user = authenticate(request, email=email, password=password)
            print(user)

            if user is not None:
                login(request, user)
                return redirect('index')

            else:
                form.add_error(None, 'Invalid username or password.')
    else:
        form = LoginForm()
    return render(request, 'signin.html', {'form': form})


def rest_password(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        print('email :',email)

        if not CustomUser.objects.filter(email=email).first():
            messages.success(request, f'Not user found with this email {email}')
            return redirect(rest_password)

        token = str(uuid.uuid4())
        profile_obj = CustomUser.objects.get(email=email)
        profile_obj.reset_password_token = token
        profile_obj.save()
        print('token',token)
        request.session['token'] = token
        request.session['email'] = email
        send_forget_password_mail(email, token)
        time.sleep(5)
        messages.success(request, 'Check Your Email To Reset Password')
        return redirect(signin)

    return render(request, 'rest_password.html')


def change_password(request, token):
    user = get_object_or_404(CustomUser, reset_password_token=token)
    if request.method == 'POST':
        form = PasswordResetForm(request.POST)
        if form.is_valid():
            new_password = form.cleaned_data['password1']
            user.set_password(new_password)
            user.reset_password_token = None
            user.save()
            messages.success(request, 'Password Reset Successful')
            return redirect('signin')
    else:
        form = PasswordResetForm(initial={'email': user.email})

    return render(request, 'change_password.html', {'form': form,'email': user.email})


def logoutfun(request):
    auth.logout(request)
    return redirect(signin)



