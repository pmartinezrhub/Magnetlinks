from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate, logout
from requests import post
from .forms import LoginForm, RegisterForm, MagnetLinkForm
from .models import MagnetLink
from django.shortcuts import render, get_object_or_404
import re
from .tasks import update_magnetlinks
from .utils import ensure_magnet_link

def home(request):
    search_query = request.GET.get('search', '')
    order = request.GET.get('order', 'seeders-desc')  

    if search_query:
        magnetlinks = MagnetLink.objects.filter(title__icontains=search_query)
    else:
        magnetlinks = MagnetLink.objects.all()

    if order == 'seeders-asc':
        magnetlinks = magnetlinks.order_by('seeders', 'leechers')  # Orden ascendente
    else:  
        magnetlinks = magnetlinks.order_by('-seeders', '-leechers')  # Orden descendente

    for link in magnetlinks:
        link.magnetlink = ensure_magnet_link(link.magnetlink)
    
    return render(request, 'home.html', {'magnetlinks': magnetlinks, 'order': order})



def sign_up(request):
    if request.method == 'GET':
        form = RegisterForm()
        return render(request, 'users/register.html', {'form': form})    

    if request.method == 'POST':
        form = RegisterForm(request.POST) 
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()
            messages.success(request, 'You have singed up successfully.')
            login(request, user)
            return redirect('home')
        else:
            return render(request, 'users/register.html', {'form': form})

def sign_in(request):
    if request.method == 'GET':
        form = LoginForm()
        return render(request,'users/login.html', {'form': form})
    
    elif request.method == 'POST':
        form = LoginForm(request.POST)
        
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request,username=username,password=password)
            if user:
                login(request, user)
                messages.success(request,f'Hi {username.title()}, welcome back!')
                return redirect('../home')        

        messages.error(request,f'Invalid username or password')
        return render(request,'users/login.html',{'form': form})

def sign_out(request):
    logout(request)
    messages.success(request,f'You have been logged out.')
    return redirect('home') 

def about(request):
    return render(request, 'about.html')

def new_magnetlink(request):
    if request.method == 'GET':
        form = MagnetLinkForm()
        return render(request, 'users/newmagnetlink.html', {'form': form})
    
    elif request.method == 'POST':
        form = MagnetLinkForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('../home')
        
        messages.error(request, 'Error on form')
        return render(request, 'users/newmagnetlink.html', {'form': form})


def magnetlink_detail(request, id):
    link = get_object_or_404(MagnetLink, id=id)
    hash_match = re.search(r'btih:([A-Fa-f0-9]{40})', link.magnetlink)

    if hash_match:
        hash_value = hash_match.group(1)  
    else:
    
        hash_value = link.magnetlink if re.match(r'^[A-Fa-f0-9]{40}$', link.magnetlink) else None
    
    if hash_value:
        magnetlink = f"magnet:?xt=urn:btih:{hash_value}"
    else:
        magnetlink = link.magnetlink  

    return render(request, 'magnetlink_detail.html', {
        'link': link,
        'hashfile': hash_value,  
        'magnetlink': magnetlink,  
    })
    
