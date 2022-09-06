import datetime
a = datetime.date.today()
b = a.strftime("%d-%b-%y")
import email
from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import render, redirect
from .forms import SignupForm
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate, login, logout
from .models import  UserTask, Activity
from .forms import  UserTaskForm

#Home Page View
def index(request):
    return render(request, 'taskmanapp/index.html')

#Sign up view Function:
def sign_up(request):
    if request.method == "POST":
        fm = SignupForm(request.POST)
        if fm.is_valid():
            messages.success(request, 'Account Created Successfully!!')
            fm.save()
    else:        
        fm = SignupForm()
    return render(request, 'taskmanapp/signup.html', {'form':fm})

#Login View Function:
def user_login(request):
    if not request.user.is_authenticated:
        if request.method=="POST":
            fm = AuthenticationForm(request=request, data=request.POST)
            if fm.is_valid():
                uname = fm.cleaned_data['username']
                upass = fm.cleaned_data['password']
                user = authenticate(username=uname , password=upass)
                if user is not None:
                    login(request, user)
                    return HttpResponseRedirect('/profile/')
        else:
            fm = AuthenticationForm()
        return render(request, 'taskmanapp/userlogin.html', {'form':fm})
    else:
        return HttpResponseRedirect('/profile/')

#Profile 
def user_profile(request):
    if request.user.is_authenticated: 
        return render(request, 'taskmanapp/profile.html', {'name':request.user})
    else:
        return HttpResponseRedirect('/login/')
    
#Logout view
def user_logout(request):
    logout(request)
    return HttpResponseRedirect('/login/')

#main page of task lists..
def taskList(request):  
    if request.user.is_authenticated: 
        user_tasks = UserTask.objects.filter(user=request.user).order_by('task_name')
        return render(request,'taskmanapp/task-list.html',{'user_tasks':user_tasks})  
    else:
        return HttpResponseRedirect('/login/')

#task adding view:
def taskCreate(request): 
    if request.user.is_authenticated: 
        if request.method == "POST":  
            form = UserTaskForm(request.POST)
            if form.is_valid(): 
                form.save(commit=False) 
                model = form.instance
                model.user = request.user
                model.save()
                Activity.objects.create(user=request.user, user_task=model.task_name, operation='create Task', updated_on=b)
                return redirect('task-list')  
        else:  
            form = UserTaskForm()  
        return render(request,'taskmanapp/task-create.html',{'form':form})
    else:
        return HttpResponseRedirect('/login/')  
#task updating view
def taskUpdate(request, id): 
    print(request.user.id) 
    if request.user.is_authenticated: 
        user_task = UserTask.objects.get(user=request.user, id=id)
        form = UserTaskForm(request.POST, instance=user_task) 
        if request.method == "POST":  
            if form.is_valid(): 
                form.save()
                Activity.objects.create(user=request.user, user_task=user_task.task_name, operation='Update Task', updated_on=datetime.datetime.now())
                return redirect('task-list') 
        else:    
            form = UserTaskForm(initial={'task_name': user_task.task_name, 'created': user_task.created, 'deadline': user_task.deadline})
        return render(request,'taskmanapp/task-update.html',{'form':form})   
    else:
        return HttpResponseRedirect('/login/') 
#task deleting view:
def taskDelete(request, id):
    if request.user.is_authenticated: 
        user_task = UserTask.objects.get(id=id)
        Activity.objects.create(user=request.user, user_task=user_task.task_name, operation='Deleted Task', updated_on=datetime.datetime.now())
        user_task.delete()
        return redirect('task-list')
    else:
        return HttpResponseRedirect('/login/') 
    
from django.views.decorators.csrf import csrf_exempt
@csrf_exempt
def update_user_task(request):
    user_task_ids = request.POST.get('user_task_ids')
    print("user_task_ids....", user_task_ids)
    user_task_status = request.POST.get('user_task_status')
    print("user_task_status....", user_task_status)
    if user_task_ids:
        user_task_ids = user_task_ids.split(",")
    user_task_status = request.POST.get('user_task_status')
    if user_task_status and int(user_task_status) == 1:
        UserTask.objects.filter(id__in=user_task_ids).update(status=1)
    UserTask.objects.exclude(id__in=user_task_ids).update(status=2)
    return JsonResponse({'result': 'success'})


def user_activity(request):
    if request.user.is_authenticated: 
        user_activities= Activity.objects.filter(user=request.user)
        print("user_activities", user_activities)
        context={
            'user_activities': user_activities,
            'name':request.user
        }
        return render(request, 'taskmanapp/activity.html', context)