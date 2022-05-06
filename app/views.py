from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from cmath import log


# Create your views here.
from app.forms import *
from django.core.mail import send_mail
from django.contrib.auth import authenticate,login

def register(request):

    
    uf=UserForm()
    pf=ProfileForm()
    d={'uf':uf,'pf':pf}
    if request.method=='POST' and request.FILES:
        ud=UserForm(request.POST)
        pd=ProfileForm(request.POST,request.FILES)
        if ud.is_valid() and pd.is_valid():
            u=ud.save(commit=False)
            u.set_password(ud.cleaned_data.get('password'))
            u.save()
            p=pd.save(commit=False)
            p.user=u
            p.save()
            return HttpResponse('registration is successfull')

    return render(request,'register.html',d)

def home(request):
    if request.session.get('username'):
        username=request.session.get('username')
        d={'username':username}
        return render(request,'home.html',d)
    return render(request,'home.html')
def user_login(request):
    if request.method=='POST':
        username=request.POST['username']
        password=request.POST['password']
        user=authenticate(username=username,password=password)
        if user and user.is_active:
            login(request,user)
            request.session['username']=username
            return HttpResponseRedirect(reverse('home'))


    return render(request,'user_login.html')
