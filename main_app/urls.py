from django.conf.urls import url,include
from . import views

from django.conf.urls import url
from django.conf.urls import include

from views import *


app_name="main_app"

from views import aboutus,faq,tc,returnpolicy,career,blog,callus, emailus


 


urlpatterns =   [
                url(r'^$',index,name='index'),
                url(r'^aboutus',aboutus,name='aboutus'),
                url(r'^faq',faq,name='faq'),
                url(r'^tc',tc,name='tc'),
                url(r'^returnpolicy',returnpolicy,name='returnpolicy'),
                url(r'^career',career,name='career'),
                url(r'^blog',blog,name='blog'),
                url(r'^callus',callus,name='callus'),
                url(r'^emailus',emailus,name='emailus'),
                url(r'^testhtml',testhtml,name='testhtml'),
                ]
