# chat/views.py
from django.shortcuts import render, redirect
from django.urls import reverse
from .models import Room

def index(request):
	rooms = Room.objects.order_by("title")
	return render(request, 'chat/index.html', {"rooms":rooms})

def room(request, room_name):
	return render(request, 'chat/room.html', {
		'room_name': room_name,
		'username': username
	})

def create_room(request):
	room_name = request.GET.get('room_name')
	if len(Room.objects.filter(title=room_name))==0:
		r = Room()
		r.title = room_name
		r.save()
	return redirect(reverse("index"))