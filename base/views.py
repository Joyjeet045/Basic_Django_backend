from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.contrib.auth import authenticate,login,logout
from .models import Room,Topic,Message
from .forms import RoomForm
# Create your views here.

def LoginPage(request):
    page='login'
    if request.user.is_authenticated:
        return redirect("home")
    if request.method=='POST':
        username=request.POST.get('username')
        password=request.POST.get('password')
        try:
            user=User.objects.get(username=username)
        except:
            messages.error(request,"User doesn't exists")
        user=authenticate(request,username=username,password=password)
        if user is not None:
            login(request,user)
            messages.success(request,f"Hello {request.user.username}")
            return redirect('home')

        else:
            messages.error(request,"Username or password doesn't exists")

      
    context={'page':page}
    return render(request,'base/login_register.html',context)
def logoutPage(request):
    logout(request)
    return redirect("home")
def registerPage(request):
    form=UserCreationForm()
    page='register'
    if request.method=='POST':
        form=UserCreationForm(request.POST)
        if form.is_valid():
            user=form.save(commit=False)
            user.username=user.username.lower()
            user.save()
            login(request,user)
            messages.success(request,f"Hello {request.user.username}")
            return redirect("home")
        else:
            messages.error(request,"An error occured during registration")
    context={'page':page,'form':form}
    return render(request,'base/login_register.html',context)

def home(request):
    q=request.GET.get('q')
    #check if q is an empty string
    if(q):
        #filtering rooms by topic_name
        rooms=Room.objects.filter(Q(topic__name__icontains=q)|Q(name__icontains=q)|Q(description__icontains=q))
        room_count=rooms.count()
        topics=Topic.objects.all()
        activities=Message.objects.filter(room__in=rooms)
        context={'rooms':rooms,'topics':topics,'room_count':room_count,'room_messages':activities}
        return render(request,'base/home.html',context)
    else:
        rooms=Room.objects.all()
        room_count=rooms.count()
        topics=Topic.objects.all()
        activities=Message.objects.all()
        context={'rooms':rooms,'topics':topics,'room_count':room_count,'room_messages':activities}
        return render(request,'base/home.html',context)


def room(request, pk):
    # room=None
    # for i in rooms:
    #     if(i['id']==int(pk)):
    #         room=i

    room=Room.objects.get(id=pk)
    room_messages=room.message_set.all()
    participants=room.participants.all()
    if request.method=='POST':
        message=Message.objects.create(
            user=request.user,
            room=room,
            body=request.POST.get('body')
        )
        room.participants.add(request.user)
        return redirect('room',pk=room.id)
    context={'room':room,'room_messages':room_messages,'participants':participants}
    return render(request,'base/room.html',context)

def userProfile(request,pk):
    user=User.objects.get(id=pk)
    #way to access child from parent
    rooms=user.room_set.all()
    room_messages=user.message_set.all()
    topics=Topic.objects.all()
    context={'user':user,'rooms':rooms,'room_messages':room_messages,'topics':topics}
    return render(request,'base/profile.html',context)


@login_required(login_url='/login')
def CreateRoom(request):
    form=RoomForm()
    if(request.method=='POST'):
        # print(request.POST)
        form=RoomForm(request.POST)
        if form.is_valid():
            room=form.save(commit=False)
            room.host=request.user
            room.save()
            return redirect('home')
    context={'form':form}
    return render(request,'base/room_form.html',context)

@login_required(login_url='/login')
def UpdateRoom(request,pk):
    room=Room.objects.get(id=pk)
    form=RoomForm(instance=room)#prefilled form
    if(request.user!=room.host):
        return HttpResponse("You are not allowed to access this room")
    if(request.method=='POST'):
        form=RoomForm(request.POST,instance=room)#prefilled form
        if form.is_valid():
            form.save()
            return redirect('home')
    context={'form':form}
    return render(request,'base/room_form.html',context)

@login_required(login_url='/login')
def DeleteRoom(request,pk):
    room=Room.objects.get(id=pk)
    if(request.method=='POST'):
        room.delete()
        return redirect('home')
    return render(request,'base/delete.html',{'obj':room})

@login_required(login_url='/login')
def deleteMessage(request,pk):
    message=Message.objects.get(id=pk)
    if request.user !=message.user:
        return HttpResponse('You are not allowed here!')
    if(request.method=='POST'):
        message.delete()
        return redirect('home')
    return render(request,'base/delete.html',{'obj':message})

