from django import forms
from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm, UserChangeForm

from user_management.models import CustomUser,UserProfile,UserAddress,CustomUserManager
from django.contrib import auth
from django.contrib.auth import authenticate
from django.contrib.auth import get_user_model

class CustomUserCreationForm(UserCreationForm):
    """
    A form that creates a user, with no privileges, from the given email and
    password.
    """
    def __init__(self, *args, **kargs):
        super(CustomUserCreationForm, self).__init__(*args, **kargs)
        #del self.fields['username']
    
    def clean(self):
            password1=self.cleaned_data.get('password1')
            password2=self.cleaned_data.get('password2')
            username=self.cleaned_data.get('email')
            try:
                user=CustomUser.objects.get(email=username)
            except:
                user=None
            if user:
                raise forms.ValidationError("Email address already registered with us")
            
            if password1!=password2:
                raise forms.ValidationError("Both password should be same")
        
    
    class Meta:
        model = get_user_model()
        #fields = "__all__"
        fields = ("email",)
    

class CustomUserChangeForm(UserChangeForm):
    """A form for updating users. Includes all the fields on
    the user, but replaces the password field with admin's
    password hash display field.
    """

    def __init__(self, *args, **kargs):
        super(CustomUserChangeForm, self).__init__(*args, **kargs)
        #del self.fields['username']

    
    class Meta:
        model = get_user_model()
        fields = "__all__"
        

        
class UserLoginForm(forms.Form):
    username = forms.CharField()
    password= forms.CharField(widget=forms.PasswordInput)
    
    def clean(self):
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')
        #user = authenticate(username=username, password=password)
        try:
            user=CustomUser.objects.get(email=username)
        except:
            user=None
        if not user:
            raise forms.ValidationError("Email not registered with us.")
        if not user.is_active and user.check_password(password):
            raise forms.ValidationError("Account is inactive, please check your mail for activation email")
        else:
            if not user.check_password(password):
                raise forms.ValidationError("Incorrect password")
        #if not user:
        #    raise forms.ValidationError("Sorry, that login was invalid. Please try again.")
        return self.cleaned_data
        
    

    def login(self, request):
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')
        user = authenticate(username=username, password=password)
        return user
class UserProfileForm(ModelForm):
    
    class Meta:
       model=UserProfile
       fields=['first_name','last_name','date_of_birth','gender']

class add_address_form(ModelForm):
    
    class Meta:
        model=UserAddress
        fields=['address_contact','address_line1','address_line2','land_mark','city','state','pin_code','mobile_no','is_primary']    


    