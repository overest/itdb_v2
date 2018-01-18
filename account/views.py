from django.shortcuts import render,redirect
from django.contrib.auth.models import User
from django.contrib import auth,messages
from django.contrib.auth.decorators import login_required
# Create your views here.

from .forms import LoginForm,ChangepwdForm

# Create your views here.

def login(request):
    # if request.user.is_authenticated():
    #     return redirect('/assets/index/')
    # if request.method == 'GET':
    #     if request.GET.get('next'):
    #         next = request.GET['next']
    #     else:
    #         next = '/account/login/'
    # else:
    #     next = '/assets/index/'
    # if next == '/account/logout/':
    #     next = '/account/login/'
    #
    # if request.method == 'POST':
    #     form = LoginForm(request.POST)
    #     if form.is_valid():
    #         auth.login(request,request.user)
    #         return redirect(request.POST['next'])
    #     else:
    #         form = LoginForm()
    #     return render(request,'account/login.html',{'form': form})
    if request.method == "GET":
        form = LoginForm()
        return render(request, 'account/login.html', {'form':form})
    else:
        form = LoginForm(request.POST)
        if form.is_valid():
            username = request.POST.get('username','')
            password = request.POST.get('password','')
            user = auth.authenticate(username=username,password=password)
            print(username,password)
            if user is not None and user.is_active:
                auth.login(request,user)
                next_url = request.GET.get("next", "/assets/index/")
                return redirect(next_url)
            else:
                return render(request, 'account/login.html', {'form':form, 'password_is_wrong':True})
        else:
            return render(request, 'account/login.html', {'form': form})

def changepwd(request):
    if request.user.is_authenticated():
        if request.method=='GET':
            form =ChangepwdForm()
            return render(request, 'account/changepwd.html', {'form':form,"stitle":"修改密码"})
        else:
            form = ChangepwdForm(request.POST)
            if form.is_valid():
                username=request.user.username
                oldpassword = request.POST.get('oldpassword','')
                user=auth.authenticate(username=username,password=oldpassword)
                if user is not None and user.is_active:
                    newpassword = request.POST.get('newpassword','')
                    user.set_password(newpassword)
                    user.save()
                    return render(request,'account/changepwddone.html',{'changepwd_success':True,"stitle":"修改密码"})
                else:
                    return render(request, 'account/changepwd.html', {'form':form, 'oldpassword_is_wrong':True,"stitle":"修改密码"})
            else:
                return render(request, 'account/changepwd.html', {'form':form,"stitle":"修改密码"})
    else:
        return redirect('/account/login/')


@login_required
def logout(request):
    auth.logout(request)
    return redirect("/account/login/")