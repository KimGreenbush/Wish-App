from django.shortcuts import render, redirect
from .models import *
import bcrypt
from django.contrib import messages
from time import strftime

#render
def index(request):
    return render(request, 'index.html')

def dashboard(request):
    if 'uuid' not in request.session:
        return redirect('/')
    context = {
        "logged_user": User.objects.get(id=request.session['uuid']),
        "user_wishes": User.objects.get(id=request.session['uuid']).uploaded_wishes.filter(granted=False),
        "granted_wishes": Wish.objects.filter(granted= True)
    }
    return render(request, 'dashboard.html', context)

def new_wish(request):
    if 'uuid' not in request.session:
        return redirect('/')
    context = {
            "logged_user": User.objects.get(id=request.session['uuid']),
    }
    return render(request, 'new_wish.html', context)

def edit_wish(request, wish_id):
    if 'uuid' not in request.session:
        return redirect('/')
    context = {
        "logged_user": User.objects.get(id=request.session['uuid']),
        "wish": Wish.objects.get(id=wish_id)
    }
    return render(request, 'edit_wish.html', context)

def stats(request):
    if 'uuid' not in request.session:
        return redirect('/')
    context = {
        "logged_user": User.objects.get(id=request.session['uuid']),
        "granted_wishes": User.objects.get(
            id=request.session['uuid']).uploaded_wishes.filter(granted=True).all(),
        "pending_wishes": User.objects.get(
            id=request.session['uuid']).uploaded_wishes.filter(granted=False).all(),
        "wishes": Wish.objects.filter(granted= True).all()
    }
    return render(request, 'stats.html', context)

#reg/login/logout
def register(request):
    errors = User.objects.register_validator(request.POST)
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value)
            return redirect('/')
    else:
        password = request.POST['password']
        pw_hash = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()
        user = User.objects.create(
            first_name=request.POST['first-name'], last_name=request.POST['last-name'], email=request.POST['email'], password=pw_hash)
        user.save()
        request.session['uuid'] = user.id
        return redirect('/wishes/')

def login(request):
    errors = User.objects.login_validator(request.POST)
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value)
            return redirect('/')
    else:
        user = User.objects.filter(email=request.POST['email'])
        logged_user = user[0]
        request.session['uuid'] = logged_user.id
        return redirect('/wishes/')

def logout(request):
    request.session.flush()
    return redirect('/')

#redirect/process
def add_a_wish(request):
    errors = Wish.objects.wish_validator(request.POST)
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect('/wishes/new/')
    else:
        Wish.objects.create(
            wish_item=request.POST['wish-item'], description=request.POST['desc'], uploaded_by=User.objects.get(id=request.session['uuid']), granted=False)
        return redirect('/wishes/')

def grant_wish(request, wish_id):
    Wish.objects.filter(id=wish_id).update(granted=True)
    return redirect('/wishes/')

def update_wish(request, wish_id):
    errors = Wish.objects.wish_validator(request.POST)
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect(f'/wishes/edit/{wish_id}/')
    else:
        Wish.objects.filter(id=wish_id).update(wish_item=request.POST['wish-item'], description=request.POST['desc'])
    return redirect('/wishes')

def delete_wish(request, wish_id):
    wish = Wish.objects.get(id=wish_id)
    wish.delete()
    return redirect('/wishes')

def like_wish(request, wish_id):
    Wish.objects.get(id=wish_id).liked_by.add(
        User.objects.get(id=request.session['uuid']))
    return redirect('/wishes')
