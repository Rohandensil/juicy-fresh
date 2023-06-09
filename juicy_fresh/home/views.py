from django.shortcuts import render,redirect
from django.contrib import auth
from django.contrib.auth.models import User 
from product.models import fruits

# Create your views here.

def index(request):
    if request.method=='POST':
        q = request.POST['query']
        obj = fruits.objects.filter(name__istartswith=q)
    else:
        obj = fruits.objects.all()
    
    return render(request,'index.html',{'data':obj})

def test(r):
    query = r.GET['query']
    return render(r,'test.html',{'val':query})

def search(r):
    return render(r,'search.html')

def login(request):
    if request.method=='POST':
        uname = request.POST['uname']
        pword = request.POST['pword']
        user = auth.authenticate(username=uname,password=pword)

        if user:
            auth.login(request,user)
            res = redirect('/')
            res.set_cookie('user',uname)
            return res
        msg = "Invalid username and password"
        return render(request,'login.html',{'msg':msg})
    else:
        return render(request,'login.html')

def register(request):
    if request.method=='POST':
        uname = request.POST['uname']
        fname = request.POST['fname']
        lname = request.POST['lname']
        email = request.POST['email']
        pword = request.POST['pword']
        rpword = request.POST['rpword']
        if pword == rpword:
            if User.objects.filter(username=uname):
                msg = "Username is already taken"
                return render(request,'register.html',{'msg':msg})
            elif User.objects.filter(email=email):
                msg = "E-mail is already registered"
                return render(request,'register.html',{'msg':msg})
            else:
                user=User.objects.create_user(first_name=fname,last_name=lname,password=pword,username=uname,email=email)
                user.save();
                auth.login(request,user)
                return redirect('/')
        else:
            msg = "Passwords do not match"
            return render(request,'register.html',{'msg':msg})
    else:
        return render(request,'register.html')

def logout(request):
    auth.logout(request)

    res = redirect('/')
    res.delete_cookie('user')
    return res

def feed(r):
    return render(r,'test.html')