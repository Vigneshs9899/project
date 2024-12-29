from django.shortcuts import render,redirect
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from .models import Blog,Contact,Skills

# Create your views here.
def index(request):
    data=Skills.objects.all()
    context={"data":data}
    return render(request,"index.html",context)

def about(request):

    return render(request,"about.html")

def contact(request):
    if not request.user.is_authenticated:
        messages.info(request,"Please Login To Contact Us")
        return render(request,'login.html')
    if request.method=="POST":
        name=request.POST['name']
        email=request.POST['email']
        phone=request.POST['num']
        desc=request.POST['desc']
        if len(phone) > 10 or len(phone) < 10:
            messages.warning(request,"Please Enter 10 digit Number")
            return redirect("/contact")
        query=Contact(name=name,email=email,phone=phone,description=desc)
        query.save()
        messages.success(request,"Thank You For Contacting Us , We Will Get Back To You Soon")
        return redirect("/contact")
    return render(request,"contact.html")

def blog(request):
    data=Blog.objects.all()
    print(data)
    context={"data":data}
    return render(request,"blog.html",context)

def signup(request):

    if request.method=="POST":
        fname=request.POST.get('fname')
        lname=request.POST.get('lname')
        email=request.POST.get('email')
        pass1=request.POST.get('pass1')
        pass2=request.POST.get('pass2')
        if pass2!=pass1:
            messages.warning(request,"Password is not matching")
            return redirect("/signup")


        try:
            if User.objects.get(username=email):
                messages.warning(request,"user already exists")
                return redirect("/signup")
        except:
            pass


        try:
            if User.objects.get(email=email):
                messages.warning(request,"email already exists")
                return redirect("/signup")
               
        except:
            pass


        user=User.objects.create_user(email,email,pass1)
        user.first_name=fname
        user.last_name=lname
        user.save()
        messages.success(request,"signup success")
        return redirect("/login")

        
    return render(request,"signup.html")

def handlelogin(request):

    if request.method=="POST":
        email=request.POST.get('email')
        pass1=request.POST.get('pass1')
        user=authenticate(username=email,password=pass1)
        if user is not None:
            login(request,user)
            messages.success(request,"login success")
            return redirect("/")
        else:
            messages.error(request,"Invalid Credentials Try Again")
            return redirect("/login")


    return render(request,"login.html")


def handlelogout(request):
    logout(request)
    messages.info(request,"Logout Success")
    return redirect("/login")
    



def search(request):
    query=request.GET['search']
    if len(query)>100:
        allPosts=Blog.objects.none()
    else:
        allPostsTitle=Blog.objects.filter(title__icontains=query)
        allPostsDescription=Blog.objects.filter(description__icontains=query)
        allPosts=allPostsTitle.union(allPostsDescription)
    if allPosts.count()==0:
        messages.warning(request,f"No Search Result Found..........{query}")
        
    params={"data":allPosts}
    
    return render(request,"search.html",params)