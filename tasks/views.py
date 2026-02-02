from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate
from django.db import IntegrityError
from .forms import TaskForm
from .models import Task, DatosPersonales, ExperienciaLaboral, Habilidad, Reconocimiento, Educacion, ProductoGarage, RecursoAcademico
from django.utils import timezone
from django.contrib.auth.decorators import login_required

# --- VISTAS PÚBLICAS (ACCESIBLES SIN LOGIN) ---

def home(request):
    # Traemos todos los perfiles para que se vean siempre en la portada
    perfiles = DatosPersonales.objects.all()
    return render(request, "home.html", {'perfiles': perfiles})

def welcome_view(request):
    # Esta función ahora hace lo mismo que home para evitar errores en urls.py
    perfiles = DatosPersonales.objects.all()
    return render(request, 'home.html', {'perfiles': perfiles})

def cv_view(request, profile_id):
    # Vista detallada de un perfil específico
    perfil = get_object_or_404(DatosPersonales, id=profile_id)
    experiencias = ExperienciaLaboral.objects.filter(perfil=perfil).order_by('-fecha_inicio')
    habilidades = Habilidad.objects.filter(perfil=perfil)
    reconocimientos = Reconocimiento.objects.filter(perfil=perfil)
    educacion = Educacion.objects.filter(perfil=perfil).order_by('-fecha_inicio')
    productos = ProductoGarage.objects.filter(perfil=perfil)
    recursos = RecursoAcademico.objects.filter(perfil=perfil)
    

    context = {
        'perfil': perfil,
        'experiencias': experiencias,
        'habilidades': habilidades,
        'reconocimientos': reconocimientos,
        'educacion': educacion,
        'productos': productos,
        'recursos': recursos
        
    }
    return render(request, 'profile_cv.html', context)

# --- SISTEMA DE USUARIOS ---

def signup(request):
    if request.method == "GET":
        return render(request, "signup.html", {"form": UserCreationForm})
    else:
        if request.POST["password1"] == request.POST["password2"]:
            try:
                user = User.objects.create_user(
                    username=request.POST["username"],
                    password=request.POST["password1"],
                )
                user.save()
                login(request, user)
                return redirect('tasks')
            except IntegrityError:
                return render(request, "signup.html", {"form": UserCreationForm, "error": "Username already exists"})
        return render(request, "signup.html", {"form": UserCreationForm, "error": "Password do not match"})

def signin(request):
    if request.method == 'GET':
        return render(request, 'signin.html', {'form': AuthenticationForm})
    else:
        user = authenticate(request, username=request.POST['username'], password=request.POST['password'])
        if user is None:
            return render(request, 'signin.html', {'form': AuthenticationForm, 'error':'Username or password is incorrect'})
        else:
            login(request, user)
            return redirect('tasks')

def signout(request):
    logout(request)
    return redirect('home')

# --- GESTIÓN DE TAREAS (REQUIERE LOGIN) ---

@login_required
def tasks(request):
    tasks = Task.objects.filter(user=request.user, datecompleted__isnull=True)
    return render(request, 'tasks.html',{'tasks':tasks, 'tipopagina':'Tareas Pendientes'})

@login_required
def tasks_completed(request):
    tasks = Task.objects.filter(user=request.user, datecompleted__isnull=False).order_by('-datecompleted')
    return render(request, 'tasks.html',{'tasks':tasks,'tipopagina':'Tareas completadas'})

@login_required
def create_task(request):
    if request.method == 'GET':
        return render(request,"create_task.html",{'form': TaskForm})
    else:
        try:
            form = TaskForm(request.POST)
            new_task = form.save(commit=False)
            new_task.user = request.user
            new_task.save()
            return redirect('tasks')
        except ValueError:
            return render(request,"create_task.html",{'form': TaskForm, 'error': 'Ingrese tipos de datos correctos'})

@login_required
def task_detail(request, task_id):
    task = get_object_or_404(Task, pk=task_id, user=request.user)
    if request.method == 'GET':
        form = TaskForm(instance=task)
        return render(request,'task_detail.html',{'task':task, 'form': form})
    else:
        try:
            form = TaskForm(request.POST, instance=task)
            form.save()
            return redirect('tasks')
        except ValueError:
            return render(request,'task_detail.html',{'task':task, 'form': form, 'error':'Error updating tasks'})

@login_required
def complete_task(request, task_id):
    task = get_object_or_404(Task, pk=task_id, user=request.user) 
    if request.method == 'POST':
        task.datecompleted = timezone.now()
        task.save()
        return redirect('tasks')

@login_required
def delete_task(request, task_id):
    task = get_object_or_404(Task, pk=task_id, user=request.user) 
    if request.method == 'POST':
        task.delete()
        return redirect('tasks')