from django.conf.urls import url,include

from django.conf.urls import url
from django.conf.urls import include


from . import views
from views import *


from django.contrib.auth import views as auth_views

app_name ="user_management"

urlpatterns =   [
                url(r'^login/',login,name='login'),
                url(r'^auth_view/',auth_view, name='auth_view'),
                url(r'^signup_success/',signup_success,name='signup_success'),
                url(r'^signup/',signup,name='signup'),
                url(r'^logout/',logout,name='logout'),
                url(r'^signup_confirm/(?P<activation_key>\w+)',signup_confirm,name='signup_confirm'),
                url(r'^account_info/',account_info,name='account_info'),
                url(r'^user_profile/',user_profile,name='user_profile'),
                url(r'^address/',address,name='address'),
                url(r'^change_password/',change_password,name='change_password'),
                url(r'^add_address/',add_address,name='add_address'),
                url(r'^edit_address/(?P<id>\d+)',edit_address,name='edit_address'),
                url(r'^delete_address/(?P<id>\d+)',delete_address,name='delete_address'),
                url(r'^change_password/',change_password,name='change_password'),
                url(r'^email_test/',email_test,name='email_test'),
                url(r'^password_reset/$', auth_views.password_reset ,{'template_name':'user_management/password_reset.html','post_reset_redirect' : 'password_reset/done/'}, name='password_reset'),
                url(r'^password_reset/done/$', auth_views.password_reset_done,{'template_name':'user_management/password_reset_done.html'}, name='password_reset_done'),
                url(r'^reset/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
                    auth_views.password_reset_confirm, name='password_reset_confirm'),
                url(r'^reset/done/$', auth_views.password_reset_complete, {'template_name':'user_management/password_reset_complete.html'}, name='password_reset_complete'),
                ]
