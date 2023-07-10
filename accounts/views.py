from django.shortcuts import render,redirect
from django.urls import reverse
from .forms import RegistrationForm
from .models import Account
from django.contrib import messages,auth
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
# Verifications

from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.core.mail import EmailMessage
from django.contrib.auth.tokens import default_token_generator
# Create your views here.

def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            email = form.cleaned_data['email']
            phone_no = form.cleaned_data['phone_no']
            password = form.cleaned_data['password']
            username = form.cleaned_data['email'].split('@')[0]
            user = Account.objects.create_user(first_name=first_name, last_name=last_name,email=email,password=password,username=username)
            user.phone_no = phone_no

            # activation User
            current_site = get_current_site(request)
            mail_subject = 'Please activate your account'
            message = render_to_string('accounts/account_verification_email.html',{
                'user': user,
                'domain' : current_site,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token' : default_token_generator.make_token(user),

            })
            to_email = email
            send_email = EmailMessage(mail_subject,message,to =[to_email])
            send_email.send()
            # messages.success(request,"Thank you for registration we have send you an activation mail ")
            return redirect(reverse('login') + '?command=verification&email=' + email)
        

    else:
        form = RegistrationForm()
    context ={
        'form': form,
    }
    return render(request, 'accounts/register.html',context)


def login(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']

        user = auth.authenticate(email=email, password=password)
        print(user.id)

        
        if user is not None:
            auth.login(request,user)
            messages.success(request,"You are now logged in ")
            # messages.success(request, 'Login successful')
            return redirect('dashboard')
        else:
            messages.error(request, "Invalid login creditional ")
            redirect ('login')

    return render(request, 'accounts/login.html')

@login_required(login_url = 'login')
def logout(request):
    auth.logout(request)
    messages.success(request, "You are logged out..")
    return redirect('login')

def activate(request,uidb64,token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = Account._default_manager.get(pk=uid)
    except (TypeError,ValueError,OverflowError,Account.DoesNotExist):
        user =None
    
    if user is not None and default_token_generator.check_token(user,token):
        user.is_active = True
        user.save()
        messages.success( request,"Congratulation YOur account is activated ")
        return redirect('login')
    else:
        messages.error("INvalid activation link")
        return redirect('register')
    
@login_required(login_url=login)
def dashboard(request):
    return render(request, 'accounts/dashboard.html')


def forget_password(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        if Account.objects.filter(email=email).exists():
            user = Account.objects.get(email__iexact=email)
            # forget password  
            current_site = get_current_site(request)
            mail_subject = 'Forget Password'
            message = render_to_string('accounts/reset_password_email.html',{
                'user': user,
                'domain' : current_site,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token' : default_token_generator.make_token(user),

            })
            to_email = email
            send_email = EmailMessage(mail_subject,message,to =[to_email])
            send_email.send()
            messages.success( request,'Reset password link has been sent in to  your mail')
            return redirect('login')
        else:
            messages.error(request,"Account with this email already does not exists")
            return redirect('forget-password')
    return render(request, 'accounts/forget_password.html')


def reset_passoword_validate(request,uidb64,token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = Account._default_manager.get(pk=uid)
    except (TypeError,ValueError,OverflowError,Account.DoesNotExist):
        user =None
    
    if user is not None and default_token_generator.check_token(user,token):
        request.session['uid'] = uid
        messages.success(request, 'Please reset your password')
        return redirect('resetPassword')
    else:
        messages.error(request, 'This link has been expired. Please try again')
        return redirect('login')
    
def resetPassword(request):
    if request.method == 'POST':
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')

        if password == confirm_password:
            uid = request.session.get('uid')
            user = Account.objects.get(pk = uid)
            user.set_password(password)
            user.save()
            messages.success(request,'Password updated successfully')
            return redirect('login')

        else :
            messages.error(request, 'Password does not match')
            return redirect('resetPassword')
    else:
        return render(request, 'accounts/resetPassword.html')
    






