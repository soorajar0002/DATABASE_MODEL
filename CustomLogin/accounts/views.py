from django.contrib import messages, auth
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from .forms import UserRegister
from django.shortcuts import render, redirect
from django.views.decorators.cache import cache_control


@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def register(request):
    if request.method == 'POST':
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']

        if password == confirm_password:
            if User.objects.filter(username=username).exists():
                messages.info(request, 'Username is already taken')
                return redirect(register)
            elif User.objects.filter(email=email).exists():
                messages.info(request, 'Email is already taken')
                return redirect(register)
            else:
                user = User.objects.create_user(username=username, password=password, email=email,
                                                first_name=first_name, last_name=last_name)
                user.save()

                return redirect('login_user')
        else:
            messages.info(request, 'Both passwords are not matching')
            return redirect(register)
    else:
        return render(request, 'registration.html')


@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def login_user(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = auth.authenticate(username=username, password=password)

        if user is not None:
            auth.login(request, user)
            return redirect('home')
        else:
            messages.info(request, 'Invalid Username or Password')
            return redirect('login_user')
    else:
        return render(request, 'login.html')


@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def home(request):
    return render(request, 'home.html')


@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def logout_user(request):
    auth.logout(request)
    return redirect('home')


@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def login_admin(request):
    if request.user.is_superuser:
        return redirect('home_admin')

    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_superuser:
                login(request, user)
                return redirect('home_admin')
            else:
                messages.error(request, 'Invalid username or password')
                return redirect('login_admin')

        else:
            return redirect('adm_login.html')
    return render(request, 'adm_login.html')


@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def home_admin(request):
    if request.user.is_authenticated:
        userdata = User.objects.all()
        search_key = request.GET.get('key') if request.GET.get('key') is not None else ''
        userdata = User.objects.filter(username__istartswith=search_key)
        return render(request, 'adm_home.html', {'userdata': userdata})


@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def logout_admin(request):
    auth.logout(request)
    return redirect('home')



def user_create(request):
    if request.user.is_superuser:
        form = UserRegister()
        if request.method == 'POST':
            form = UserRegister(request.POST)
            if form.is_valid():
                form.save()
                return redirect('home_admin')
            else:
                messages.error(request, 'invalid details')

        return render(request, 'Add_user.html', {'form': form})



def update_user(request, id):
    if request.user.is_superuser:
        userid = User.objects.get(pk=id)
        form = UserRegister(instance=userid)
        if request.method == 'POST':
            userid = User.objects.get(pk=id)
            form = UserRegister(request.POST, instance=userid)
            if form.is_valid():
                form.save()
                return redirect('home_admin')
            else:
                userid = User.objects.get(pk=id)
                form = UserRegister(instance=userid)
                messages.error(request, 'invalid details')
        return render(request, 'update.html', {'form': form})



def delete_user(request, id):
    if request.user.is_superuser:
        userid = User.objects.get(pk=id)
        userid.delete()
        return redirect('home_admin')
