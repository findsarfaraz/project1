from django.shortcuts import render
from django.template import loader
# Create your views here.
from django.shortcuts import HttpResponse

def index(request):
    return render(request,'main_app/index.html',None)

def aboutus(request):
    return render(request,'main_app/aboutus.html',None)
   
def faq(request):
    return render(request,'main_app/faq.html',None)

def tc(request):
    return render(request,'main_app/tc.html',None)

def returnpolicy(request):
    return render(request,'main_app/returnpolicy.html',None)

def career(request):
    return render(request,'main_app/career.html',None)

def blog(request):
    return render(request,'main_app/blog.html',None)

def emailus(request):
    return render(request,'main_app/emailus.html',None)

def callus(request):
    return render(request,'main_app/callus.html',None)
def testhtml(request):
    return render(request,'main_app/test.html',None)