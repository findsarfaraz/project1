
from django.db import models
from django.contrib.auth.models import AbstractBaseUser,BaseUserManager,PermissionsMixin
from django.core.mail import send_mail
from django.utils.translation import ugettext_lazy as _
#now=time.strftime('%Y-%M-%D %H:%m:%S.%u%Z')
import datetime
from datetime import timedelta

from django.utils import timezone

tomorrow = timezone.now() + timedelta(days=1)
current_time= timezone.now()

class CustomUserManager(BaseUserManager):
    def _create_user(self,email,password,is_staff,is_superuser, **extra_fields):

        if not email:
            raise ValueError('The given email must be set')
        
        email=self.normalize_email(email)
        user= self.model(email=email,
                         is_staff=is_staff,
                         is_active = True,
                         is_superuser =is_superuser,
                         last_login=timezone.now(),
                         date_joined=timezone.now(),
                        **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user
    
    def create_user(self, email,password=None,**extra_fields):
        return self._create_user(email,password,False,False,**extra_fields)
    
    def create_superuser(self, email,password,**extra_fields):
        return self._create_user(email,password,True,True,**extra_fields)
    
class CustomUser(AbstractBaseUser,PermissionsMixin):
    username =models.CharField(max_length =256, unique = True,blank = True,null= True)
    email =models.EmailField(blank=False, unique =True)
    date_joined  = models.DateTimeField(_('date joined'), default=current_time)
    is_active    = models.BooleanField(default=True)
    is_admin     = models.BooleanField(default=False)
    is_staff     = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
   
    USERNAME_FIELD ='email'
    REQUIRED_FIELD =['user_name','date_joined']
    
    objects=CustomUserManager()
    
    class Meta:
        verbose_name=_('user')
        verbose_name_plural=_('users')
    
    def get_absolute_url(self):
        return "/user/%s" %urlquote(self.email)
    
    def get_full_name(self):
      
        a=UserProfile.objects.get(email_id=self.id)
        self.first_name=a.first_name
        self.last_name= a.last_name
        if not self.first_name and not self.last_name:
            full_name =self.email
        else:
            full_name = '%s %s' %(self.first_name,self.last_name)
        return full_name.strip()

    def get_short_name(self):
        self.first_name='a'
        return self.first_name
    
    def email_user(self,subject,message,from_email=None):
        send_mail(subject,message,from_email,[self.email])


        #code

class UserProfile(models.Model):

    email = models.OneToOneField(CustomUser,unique =True,primary_key=True)
    first_name=models.CharField(max_length =256, blank = True)
    last_name=models.CharField(max_length =256, blank = True)
    activation_key = models.CharField(max_length=40,blank=True)
    gender = models.CharField(max_length=6, null=True,blank=True,choices=(
        ('male', 'Male'),
        ('female', 'Female'),))
    date_of_birth=models.DateField(null=True,blank=True)
    key_expires = models.DateTimeField(default=tomorrow)
      
    def __str__(self):
        full_name = '%s %s' %(self.first_name,self.last_name)
        return full_name

    class Meta:
        verbose_name=u'User profile'
        verbose_name_plural=u'User profiles'
    
    models.OneToOneField(CustomUser, related_name='Userprofile')

class UserAddress(models.Model):
    address_contact=models.CharField(max_length=300,blank=False)
    address_line1=models.CharField(max_length=300,blank=False)
    address_line2=models.CharField(max_length=300,blank=True)
    land_mark=models.CharField(max_length=100,blank=False)
    city=models.CharField(max_length=140,blank=False)
    state=models.CharField(max_length=100,blank=False)
    pin_code = models.BigIntegerField(blank=False)
    mobile_no=models.CharField(max_length=13,blank=True)
    last_shipped_flag=models.BooleanField(default=False)
    is_active_flag=models.BooleanField(default=True)
    is_primary=models.BooleanField(default=False)
    creation_date=models.DateTimeField(auto_now_add=True,editable=False,blank=False,null=True)
    updation_date=models.DateTimeField(auto_now=True,editable=False,blank=False,null=True)
    email=models.ForeignKey(UserProfile,default=0)

    
    def __str__(self):
        return self.address_contact
    

    class Meta:
        verbose_name=u'User Address'
        verbose_name_plural=u'User Addresses'

    
    