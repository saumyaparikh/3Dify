import imp
from .models import StereoImages
from django.shortcuts import redirect, render,HttpResponse
from django.http import request
from .models import StereoImages
from django.contrib.auth.models import User
from . import model3dfrom2d as m3d
import urllib.request
from django.contrib import  messages
import webbrowser
from django.contrib.auth import authenticate,login,logout

from .forms import *
img=""
def home(request):
    flag=0
    
    if request.method == 'POST':
        usr = request.user
        
        form=StereoImgForm(request.POST, request.FILES)
  
        if form.is_valid():
            obj=form.save() #tells dont save yet we have other things to do with it
            my3dmodel=m3d.Mesh()
            global img
            try:
                img=str(form.instance.StereoImg.url)
            except:
                messages.error(request, "Please upload image")
                return render(request,'home.html',{'form':form})
            print("Image name: ",img[1:])
            x=my3dmodel.createmesh(img[1:])
            if x==0:
                 messages.error(request, "Please upload valid image")
                 return render(request,'home.html',{'form':form})
            
            obj.email=request.user.email    
            obj.save()
            flag=1
            messages.success(request, "Successfully Completed")
            return render(request,'home.html',{'form':form,'img':img[1:],'flag':flag})

    else:
        form = StereoImgForm()
    
    
    return render(request, 'home.html', {'form' : form})
   
def download(request):
    form=StereoImgForm(request.POST, request.FILES)
    
    imgurl="https://app3dify.herokuapp.com/"+img[1:]+".ply"
    print(imgurl)
    #urllib.request.urlretrieve(imgurl, imgurl)   
    webbrowser.open(imgurl)
    return redirect('home')
    # return render(request, 'home.html', {'form' : form})
def download2(request):
    dashimage = request.POST.get('dashimage',None)
    print("$$",dashimage)
    imgurl="https://app3dify.herokuapp.com/"+dashimage+".ply"
    print(imgurl)
    
    webbrowser.open(imgurl)
    return redirect('dashboard')
    
def logoutuser(request):
    logout(request)
    messages.success(request,"Logged out")
    return redirect('home')

def loginuser(request):
    uname = request.POST['uname']
    passw = request.POST['passw']
    l=User.objects.all()
    print(l)
    for u in l:
        print(u)
    usr=authenticate( username=uname, password=passw)
    print(usr)
    if usr is not None:
        login(request, usr)
        messages.success(request, "Logged in successfully")
        return redirect("home")
    else:
        messages.error(request, "Invalid credentials")
        return redirect('home')
def signup(request):

    # messages.error(request,"checking error")

    if(request.method=='POST'):
        uname=request.POST['uname']
        email=request.POST['email']
        passw=request.POST['pass']
        cnfpass=request.POST["cnfpass"]
        print(uname,email,passw,cnfpass)
        print(type(passw))
        print(passw==cnfpass)
        if not uname.isalnum():
            messages.error(request,"Username must only contain no and letters")
            return redirect('home')

        if (passw != cnfpass):
            messages.error(request,"Passwords should match")
            return redirect('home')

        if(passw==cnfpass):

            myuser=User.objects.create_user(uname, email, passw)
            myuser.save()
            messages.success(request, "User registered successfully")
            return redirect('home')

    else:
        return HttpResponse('404..Not Found')



    return render(request,'index.html')


def success(request):
    return render('home')

def dashboard(request):
    print("inside dash")
    h2=StereoImages.objects.filter(email=request.user.email)
    print("H2 is:",h2)
    for d in h2:
        print("The data of user: ",d)
    return render(request,'dashboard.html',{'data':h2})
def aboutus(request):
    return render(request,'aboutus.html')