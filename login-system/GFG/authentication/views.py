from django.shortcuts import render,redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.contrib.auth import logout as user_logout
from django.contrib.auth import login as auth_login
from django.contrib import messages
from GFG import settings
from django.core.mail import send_mail


def home(request):
    return render(request,"authentication/home.html")

def signup(request):
    if request.method == "POST":
        firstname = request.POST.get("fname")
        lastname = request.POST.get("lname")
        username = request.POST.get("uname")
        email = request.POST.get("email")
        password = request.POST.get("pass")
        password2 = request.POST.get("pass2")

        if password != password2:
            messages.error(request,"pasword dosen't match")

        if not username.isalnum():
            messages.error(request,"username must be alpha-numeric")
            redirect("home")

        if User.objects.filter(email=email):
            messages.error(request,"email already exist! try another one")

        if User.objects.filter(username=username):
            messages.error(request,"username already exist! try another one")
            return redirect("home")
        
        if len(username)>10:
            messages.error(request,"username is to long")



        user = User.objects.create_user(username,email,password)
        user.first_name = firstname
        user.last_name = lastname
        #user.check_password(password2)
        user.save()

        messages.success(request,"account sucessfully created")


        #welcome email

        subject = "Welcome to Practice Hub!"
        message = "Hello " + user.first_name + "!! \n" + "Welcome to Practice Hub! \n Than You For Visting Our Website. \n We have also sent you a confirmation code, please confirm your email address in order to activate your account. \n\n Thanking You.\n Olufemi Odunayo."
        from_eamil = settings.EMAIL_HOST_USER
        to_list = [email]
        send_mail(subject,message,from_eamil,to_list,fail_silently=True)



        return redirect("login")
    return render(request,"authentication/signup.html")

def login(request):
    if request.method == "POST":
        username = request.POST.get("uname")
        password = request.POST.get("pass")

        user = authenticate(username=username,password=password)

        if user is not None:
            auth_login(request, user)
            fname = user.first_name
            return render(request,"authentication/home.html", {"fname":fname})

        else:
            messages.error(request,"Bad Cridentials")
            return redirect("signup")

    return render(request,"authentication/login.html")

def logout(request):
    user_logout(request)
    messages.success(request,"Logged Out Sucessfully")
    return redirect('home')