from django.shortcuts import render
from django.contrib import auth
from django.contrib.auth.decorators import login_required

from django.http import HttpResponseRedirect,HttpResponse
from django.views.decorators.csrf import requires_csrf_token,csrf_protect
from .forms import UserLoginForm,CustomUserCreationForm,UserProfileForm,add_address_form
from .models import (CustomUser,CustomUserManager,UserProfile,UserAddress)
from django.core.mail import send_mail
from django.core.mail import EmailMessage
from django.shortcuts import get_object_or_404
from django.template import Context
 

from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm

import hashlib
import random
from django.utils import timezone
from datetime import timedelta

from django.template import Context
from django.template.loader import get_template

from django.contrib.auth import views as auth_views





# Create your views here.

@csrf_protect
def login(request):
    form=UserLoginForm()
    if request.user.is_authenticated:
        return HttpResponseRedirect('/')
    else:
        return render(request,'user_management/login.html',{'form':form})

@csrf_protect    
def auth_view(request):
    form=UserLoginForm(request.POST or None)
    if request.POST and form.is_valid():
        user = form.login(request)
        
        if user:
            auth.login(request, user)
            return HttpResponseRedirect('/')# Redirect to a success page.
    
    return render(request, 'user_management/login.html', {'form': form })
            
def logout(request):
    auth.logout(request)
    return render(request,'main_app/index.html',None)

@csrf_protect 
def signup(request):
    form= CustomUserCreationForm(request.POST or None)
    if request.POST and form.is_valid():
        form.save(commit=False)
        email=form.cleaned_data['email']
        password=form.cleaned_data['password1']
        CustomUser.objects.create_user(email=email,password=password)
        user=CustomUser.objects.get(email=email)
        user.is_active=0
        user.save()
        
        salt = hashlib.sha1(str(random.random())).hexdigest()[:5]            
        activation_key = hashlib.sha1(salt+email).hexdigest()            
        key_expires = timezone.datetime.today() + timedelta(days=2)
        
        
        up=UserProfile(email_id=user.id,activation_key=activation_key, 
                key_expires=key_expires)
        
        up.save()
        #link ="http://127.0.0.1:8000/signup_confirm/%s" % (activation_key)
        #link ="test"
        #name ="Friend"
        c = Context({'link':link,'name': name})
        
        
        #email_body = get_template('user_management/email.html').render(c)
        #email_subject = 'Account confirmation'
        #msg=EmailMessage(email_subject, email_body, to=[email], from_email='registration@arhamcollections.com')
        # msg.content_subtype="html"
        
        #msg.send()
        #send_mail(email_subject, email_body, ,[email], fail_silently=False)
        
        if user:
            return HttpResponseRedirect('/signup_success')
    
    return render(request,'user_management/signup.html',{'form':form})


def signup_success(request):
    return render(request,'user_management/signup_success.html',None)

            
def signup_confirm(request,activation_key):
    #check if user is already logged in and if he is redirect him to some other url, e.g. home
    if request.user.is_authenticated():
        HttpResponseRedirect('/')
    
    # check if there is UserProfile which matches the activation key (if not then display 404)
    user_profile = get_object_or_404(UserProfile, activation_key=activation_key)
    
    #check if the activation key has expired, if it hase then render confirm_expired.html
    if user_profile.key_expires < timezone.now():
        return  render(request,'user_management/confirm_expired.html',None)
    #if the key hasn't expired save user and set him as active and render some template to confirm activation
    
    cu=CustomUser.objects.get(email=user_profile.email)
    cu.is_active = True
    cu.save()
    return render(request,'user_management/confirm.html',None)

def email_test(request):
    user=CustomUser.objects.get(email='test@arhamcollections.com')
    email='test@arhamcollections.com'
    salt = hashlib.sha1(str(random.random())).hexdigest()[:5]            
    activation_key = hashlib.sha1(salt+email).hexdigest()            
    key_expires = timezone.datetime.today() + timedelta(days=2)
        
    link ="http://127.0.0.1:8000/signup_confirm/%s" % (activation_key)
    name ="Friend"
    c = Context({'link':link,'name': name})
    email_body = get_template('user_management/email.html').render(c)
    return HttpResponse(email_body)

@login_required(login_url='user_management:login')
@csrf_protect
def account_info(request):
    try:
        instance=UserProfile.objects.get(email_id=request.user.id)
    except:
        u=UserProfile.objects.create(email_id=request.user.id)
        u.save()
        instance=UserProfile.objects.get(email_id=request.user.id)
    form=UserProfileForm(request.POST or None, instance=instance)
   
    if request.method=="POST":
        if form.is_valid():
            instance=form.save(commit=False)
            instance.save()
            form=UserProfileForm(instance=instance)
            return render(request,'user_management/account_info.html',{'form':form})
        else:
            return render(request,'user_management/account_info.html',{'form':form})
    else:
        return render(request,'user_management/account_info.html',{'form':form})
    
        

def user_profile(request):
    
    form=UserProfileForm()
    return render(request,'user_management/user_profile.html',{'form':form})

def address(request):
    try:
        UA=UserAddress.objects.filter(email_id=request.user.id,is_active_flag=1)
    except UserAddress.DoesNotExist:
        raise Http404("No MyModel matches the given query.")
    
    i=1        
    for address in UA:
        address.row_id =i
        i=i+1
    return render(request,'user_management/address.html',{'UA':UA})

@login_required(login_url='user_management:login')
@csrf_protect
def add_address(request):
    form=add_address_form(request.POST or None)
    
    if request.method=="POST":

        if form.is_valid():
            form.save(commit=False)
            is_primary = form.cleaned_data['is_primary']
            
            if is_primary:
                UA=UserAddress.objects.filter(email_id = request.user.id , is_active_flag=1 ).update(is_primary=0)
                
                
            U = UserAddress.objects.create(address_contact=form.cleaned_data['address_contact'],
                            address_line1=form.cleaned_data['address_line1'],
                            address_line2=form.cleaned_data['address_line2'],
                            land_mark=form.cleaned_data['land_mark'],
                            city=form.cleaned_data['city'],
                            state=form.cleaned_data['state'],
                            pin_code=form.cleaned_data['pin_code'],
                            mobile_no=form.cleaned_data['mobile_no'],
                            is_primary=form.cleaned_data['is_primary'],
                            email_id=request.user.id)
            U.save()
            return HttpResponseRedirect('/address/')
            #return render(request,'user_management/add_address.html',{'form':form})
        else:
            return render(request,'user_management/add_address.html',{'form':form})
    else:
        return render(request,'user_management/add_address.html',{'form':form})
    
@login_required(login_url='user_management:login')
@csrf_protect
def edit_address(request,id):
    instance=UserAddress.objects.get(id=id)
    form=add_address_form(request.POST or None,instance=instance)
    
    if request.method=="POST":
        
        if form.is_valid():
            is_primary = form.cleaned_data['is_primary']
            
            if is_primary:
                UA=UserAddress.objects.filter(email_id = request.user.id , is_active_flag=1 ).update(is_primary=0)
            instance=form.save(commit=False)
            instance.save()
            return HttpResponseRedirect('/address/')
        else:
            return render(request,'user_management/edit_address.html',{'form':form})
    else:
        return render(request,'user_management/edit_address.html',{'form':form})

def delete_address(request,id):
    
    instance=UserAddress.objects.get(id=id)
    instance.is_active_flag=0
    instance.save()
    return HttpResponseRedirect('/address/')


@login_required(login_url='user_management:login')
@csrf_protect
def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            print form
            user = form.save()
            update_session_auth_hash(request, user)  # Important!
            return render(request,'user_management/change_password_done.html',None)    
        return render(request,'user_management/change_password.html',{'form': form})            
    else:
        form = PasswordChangeForm(request.user)
        return render(request, 'user_management/change_password.html', {'form': form})
    

        