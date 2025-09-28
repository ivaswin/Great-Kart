from django.shortcuts import render,redirect
from django.http import HttpResponse
from .forms import RegistrationForm
from .models import Accounts
from django.contrib import messages,auth
from django.contrib.auth.decorators import login_required

#Verification Email
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode,urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import EmailMessage

def register(request):
    if request.method =='POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            phone_number = form.cleaned_data['phone_number']
            email = form.cleaned_data['email']
            password =  form.cleaned_data['password']
            username = email.split('@')[0]
            user = Accounts.objects.create_user(first_name = first_name,last_name=last_name,email=email,username=username,password=password)
            user.phone_number = phone_number
            user.save()
            #user activation
            current_site = get_current_site(request)
            mail_subject = 'Please activate your account'
            message = render_to_string('accounts/account_verification_email.html',{
                'user':user,
                'domain' : current_site,
                'uid' :urlsafe_base64_encode(force_bytes(user.pk)),
                'token' : default_token_generator.make_token(user),

            })
            to_email = email
            send_email = EmailMessage(mail_subject,message,to=[to_email])
            send_email.send()
            

            #messages.success(request,'Registration succesful.')
            return redirect('/accounts/login/?command=verification&email='+ email)
    else:        
        form = RegistrationForm()

    
    context = {
        'form':form,
    }

    return render(request,'accounts/register.html',context)

def login(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']

        user = auth.authenticate(email=email,password=password)

        if user is not None:
            auth.login(request,user)
            messages.success(request, 'You are now loged In')
            return redirect('dashboard')
        else:
            messages.error(request,'Invalid login credentials')
            return redirect('login')


    return render(request,'accounts/login.html')
  
@login_required(login_url='login')
def logout(request):
    auth.logout(request)
    messages.success(request,'You are loged Out')
    return redirect('login')


def activate(request,uidb64,token):       
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = Accounts._default_manager.get(pk=uid)
    except(TypeError,ValueError,Accounts.DoesNotExist,OverflowError):
        user=None

    if user is not None and default_token_generator.check_token(user,token):
        user.is_active = True
        user.save()
        messages.success(request, 'Your account is activated')
        return redirect('login')
    else:
        messages.error(request, 'Invalid activaton Link')
        return redirect('register')
    
    
@login_required(login_url='login')
def dashboard(request):
    return render(request,'accounts/dashboard.html')


def forgotPassword(request):

    if request.method == 'POST':
        email = request.POST['email']
        if Accounts.objects.filter(email=email).exists():
            user = Accounts.objects.get(email__exact=email)

             #password reset
            current_site = get_current_site(request)
            mail_subject = 'Reset Your Password'
            message = render_to_string('accounts/reset_password_email.html',{
                'user':user,
                'domain' : current_site,
                'uid' :urlsafe_base64_encode(force_bytes(user.pk)),
                'token' : default_token_generator.make_token(user),

            })
            to_email = email
            send_email = EmailMessage(mail_subject,message,to=[to_email])
            send_email.send()
            messages.success(request,'Password reset email has send to your email address')
            return redirect('login')
        
        else:
            messages.error(request,'Account doesnot exist')
            return redirect('forgotPassword')
    return render(request,'accounts/forgotPassword.html')


def reset_password_validate(request,uidb64,token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = Accounts._default_manager.get(pk=uid)
    except(TypeError,ValueError,Accounts.DoesNotExist,OverflowError):
        user=None

    if user is not None and default_token_generator.check_token(user,token):
        request.session['uid'] = uid
        messages.success(request,'please reset your password')
        return redirect('resetPassword')
    else:
        messages.error(request,'This link has been expired')
        return redirect('login')
    
def resetPassword(request):
    if request.method == 'POST':
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']

        if password == confirm_password:
            uid = request.session.get('uid')
            user = Accounts.objects.get(pk=uid)
            user.set_password(password)
            user.save()
            messages.success(request,'Password Reset Success')
            return redirect('login')

        else:
            messages.error(request,'Password doesnot match')
            return redirect('reset_password')
    else:
        return render(request,'accounts/reset_password.html')



