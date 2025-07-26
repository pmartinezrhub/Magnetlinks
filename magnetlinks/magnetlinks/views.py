from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth import update_session_auth_hash, logout
from requests import post
from .forms import LoginForm, RegisterForm, MagnetLinkForm, AccountForm
from .models import MagnetLink
from django.shortcuts import render, get_object_or_404
import re
from .tasks import update_magnetlinks
from .utils import ensure_magnet_link
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden

def home(request):
    search_query = request.GET.get('search', '')
    order = request.GET.get('order', 'seeders-desc')  

    if search_query:
        magnetlinks = MagnetLink.objects.filter(filename__icontains=search_query)
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

@login_required
def sign_out(request):
    logout(request)
    response = redirect('home')  # Primero creas la respuesta
    response.delete_cookie('sessionid')  # Ahora sí puedes borrar la cookie
    return response


def about(request):
    return render(request, 'about.html')

@login_required
def new_magnetlink(request):
    if request.method == 'GET':
        form = MagnetLinkForm()
        return render(request, 'users/newmagnetlink.html', {'form': form})
    
    elif request.method == 'POST':
        form = MagnetLinkForm(request.POST)
        if form.is_valid():
            magnet = form.save(commit=False)
            magnet.user = request.user  
            magnet.save()
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

@login_required
def account(request):
    if request.method == 'POST':
        form = AccountForm(user=request.user, data=request.POST)
        if form.is_valid():
            user = form.save()
            if user is None:
                # Usuario borrado -> cerrar sesión
                logout(request)
                return redirect('account_deleted')  # Crea esta URL o página de confirmación
            else:
                # Solo cambio de password
                update_session_auth_hash(request, user)
                #return redirect('password_change_done')  # O tu propia página
                logout(request)
                response = redirect('password_change_done')  # Primero creas la respuesta
                response.delete_cookie('sessionid')  # Ahora sí puedes borrar la cookie
                return response
    else:
        form = AccountForm(user=request.user)

    return render(request, 'users/account.html', {'form': form})

def account_deleted(request):
    return render(request, 'users/account_deleted.html')

def password_change_done_custom(request):
    return render(request, 'users/password_change_done.html')

@login_required
def magnetlink_delete(request, pk):
    magnetlink = get_object_or_404(MagnetLink, pk=pk)
    if magnetlink.user != request.user:
        return HttpResponseForbidden("No tienes permiso para borrar este magnetlink.")

    if request.method == 'POST':
        magnetlink.delete()
        messages.success(request, 'Magnetlink borrado correctamente.')
        return redirect('home')  # o la vista que muestre la lista
    else:
        return HttpResponseForbidden("Método no permitido.")
