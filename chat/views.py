# chat/views.py
from django.shortcuts import render, redirect
from django.urls import reverse
from .models import Room
import random

def index(request):
	rooms = Room.objects.order_by("title")
	return render(request, 'chat/index.html', {"rooms":rooms})

def room(request, room_name, username):
	return render(request, 'chat/room.html', {
		'room_name': room_name,
		'username': username
	})

def create_room(request):
	room_name = request.GET.get('room_name')
	username = request.GET.get('username')
	print (room_name)
	print(username)
	if len(Room.objects.filter(title=room_name))==0:
		r = Room()
		r.title = room_name
		r.save()
	url = "/chat/" + room_name + "/" + username + "/"
	return redirect(url)