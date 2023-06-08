from django.shortcuts import render,redirect,get_object_or_404
from django.contrib.auth.forms import UserCreationForm,AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate
from django.http import HttpResponse
from django.db import IntegrityError
from .form import TaskForm
from .models import Tasks
from django.utils import timezone
from django.contrib.auth.decorators import login_required
# Create your views here.


def home(request):
    return render(request, 'home.html')

def signup(request):

    if request.method == "GET":
        form = UserCreationForm()
        return render(request, 'signup.html', {'form': form})
    else:
        if request.POST['password1'] == request.POST['password2']:
            try:
                user = User.objects.create_user(username=request.POST['username'],
                password=request.POST['password1'])
                user.save()
                login(request, user)
                return redirect('task')
            except IntegrityError():
                return render(request, 'signup.html',{
                    'form': UserCreationForm,
                    'message': "user already exists"
                })
           
        else:
            return render(request, 'signup.html',{
                'form':UserCreationForm,
                'message':"password do no match"
            })
@login_required
def task_complete(request,task_id):
    task = get_object_or_404(Tasks,pk=task_id,user=request.user)
    if request.method == 'POST':
        task.datecompleted = timezone.now()
        task.save()
        return redirect('task')

def delete_task(request,task_id):
    task = get_object_or_404(Tasks,pk=task_id,user=request.user)
    if request.method == 'POST':
        task.delete()
        return redirect('task')

@login_required
def task(request):
    task = Tasks.objects.filter(user=request.user,datecompleted__isnull=True)
    return render(request, 'task.html',{
        'tasks':task
    })

@login_required
def complete_task(request):
    task = Tasks.objects.filter(user=request.user,datecompleted__isnull=False)
    return render(request, 'task_complete.html',{
        'tasks':task
    })    

@login_required
def task_detail(request,task_id):
    if request.method == "GET":
        result = get_object_or_404(Tasks,pk=task_id)
        form = TaskForm(instance=result)
        return render(request, 'task_detail.html',{'task':result,'form':form})
    else:
        task = get_object_or_404(Tasks,pk=task_id)
        form = TaskForm(request.POST,instance=task)
        form.save()
        return redirect('task')

    
@login_required
def signout(request):
    logout(request)
    return redirect('/')
def signin(request):
    print(request)
    if request.method == "GET":
        return render(request, 'signin.html',{
        'form': AuthenticationForm
    })
    else:
        user =authenticate(request,username=request.POST['username'],
        password=request.POST['password'])
        if user is None:
            return render(request, 'signin.html',{
            'form': AuthenticationForm,
            'error':"username or password incorrect"
            })
        else:
            login(request, user)
            return redirect('task')

@login_required
def create_task(request):
    if request.method == "GET":
        return render(request, 'created_task.html',{
            'form':TaskForm
        })
    else:
        try:
            form = TaskForm(request.POST)
            new_task = form.save(commit=False)
            new_task.user = request.user
            new_task.save()
            return redirect('task')
        except  ValueError:
            return render(request, 'created_task.html',
            {'error': "please provide validate data "})
