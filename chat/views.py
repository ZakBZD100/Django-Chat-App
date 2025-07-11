
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from .models import Room, Message, Role
from .forms import RoomForm, MessageForm
from django.core.paginator import Paginator
from django.http import JsonResponse
from datetime import timedelta
from django.utils import timezone
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils import timezone
import json
from .models import Room, Message, Role
from .forms import MessageForm

def logout_view(request):
    logout(request)
    return redirect('login')

def room_detail(request, id):
    if not request.user.is_authenticated:
        return redirect('login')
    
    room = get_object_or_404(Room, id=id)
    messages = Message.objects.filter(room=room).order_by('date')
    return render(request, 'chat/room_detail.html', {'room': room, 'messages': messages})

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('room_list')
    else:
        form = UserCreationForm()
    return render(request, 'chat/register.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('room_list')
    else:
        form = AuthenticationForm()
    return render(request, 'chat/login.html', {'form': form})

def room_list(request):
    if not request.user.is_authenticated:
        return redirect('login')
    
    rooms_list = Room.objects.all()
    paginator = Paginator(rooms_list, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'chat/room_list.html', {'page_obj': page_obj})

def create_room(request):
    if not request.user.is_staff:
        return redirect('room_list') 

    if request.method == 'POST':
        form = RoomForm(request.POST)
        if form.is_valid():
            room = form.save()

            Role.objects.create(user=request.user, room=room, role='admin')
            return redirect('room_detail', id=room.id)
    else:
        form = RoomForm()

    return render(request, 'chat/create_room.html', {'form': form})

def home(request):
    if not request.user.is_authenticated:
        return redirect('login')
    return redirect('room_list')

@csrf_exempt
def send_message(request, id):
    if request.method == 'POST':
        try:
            room = get_object_or_404(Room, id=id)
            data = json.loads(request.body)
            message_text = data.get('text', '').strip()
            
            if message_text:
                message = Message.objects.create(
                    room=room,
                    user=request.user,
                    text=message_text,
                    date=timezone.now()
                )
                
                return JsonResponse({
                    'status': 'success',
                    'id': message.id,
                    'username': message.user.username,
                    'message': message.text,
                    'date': message.date.strftime('%Y-%m-%d %H:%M:%S')
                })
            
            return JsonResponse({
                'status': 'error',
                'message': 'Message cannot be empty'
            })
            
        except json.JSONDecodeError:
            return JsonResponse({
                'status': 'error',
                'message': 'Invalid data format'
            }, status=400)
            
    return JsonResponse({
        'status': 'error',
        'message': 'Method not allowed'
    }, status=405)

def get_messages(request, room_id):
    last_message_id = int(request.GET.get('last_id', 0))
    messages = Message.objects.filter(room_id=room_id)
    if last_message_id > 0:
        messages = messages.filter(id__gt=last_message_id)
    messages = messages.select_related('user').order_by('date')[:50]
    
    messages_data = [{
        'id': msg.id,
        'username': msg.user.username,
        'text': msg.text,
        'date': timezone.localtime(msg.date).strftime('%Y-%m-%d %H:%M:%S')
    } for msg in messages]
    
    if messages_data:
        last_message_id = max(msg['id'] for msg in messages_data)
    
    return JsonResponse({
        'messages': messages_data,
        'last_id': last_message_id
    })