from typing import Any
from django.forms.models import BaseModelForm
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic import ListView
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Event, Collide, Rsvp, User
from .forms import CustomSignupForm, RsvpForm

# Create your views here.
def home(request):
    return render(request, 'home.html')


@login_required
def events_index(request):
    events = Event.objects.all()
    return render(request, 'events/index.html', { 'events': events })


@login_required
def events_detail(request, event_id):
    event = Event.objects.get(id=event_id)
    collides = Collide.objects.filter(event=event)
    return render(request, 'events/detail.html', { 'event': event, 'collides': collides })


class EventCreate(LoginRequiredMixin, CreateView):
    model = Event
    fields = ['title', 'date', 'category', 'description', 'details']
    success_url = '/events'
    
    def form_valid(self, form):
        form.instance.creator = self.request.user
        return super().form_valid(form)
    
    
class EventUpdate(LoginRequiredMixin, UpdateView):
    model = Event
    fields = ['title', 'date', 'category', 'description', 'details']
    success_url = '/profile/events'
    
    def dispatch(self, request, *args, **kwargs):
        event = self.get_object()
        if event.creator != request.user:
            return redirect('events_index')
        return super().dispatch(request, *args, **kwargs)
    
    
class CollideCreate(LoginRequiredMixin, CreateView):
    model = Collide
    fields = ['location', 'time', 'details']
    
    def form_valid(self, form):
        form.instance.host = self.request.user
        event_id = self.kwargs.get('event_id')
        event = get_object_or_404(Event, pk=event_id)
        form.instance.event = event
        return super().form_valid(form)
    
    
class CollideUpdate(LoginRequiredMixin, UpdateView):
    model = Collide
    fields = ['location', 'time', 'details']
    success_url = '/profile/collides'

    def dispatch(self, request, *args, **kwargs):
        collide = self.get_object()
        if collide.host != request.user:
            return redirect('/profile/collides')
        return super().dispatch(request, *args, **kwargs)


@login_required
def collides_detail(request, collide_id):
    collide = Collide.objects.get(id=collide_id)
    rsvp = Rsvp.objects.filter(collide=collide)
    has_rsvpd = collide.rsvp_set.filter(attendee=request.user).exists()
    return render(request, 'collides/detail.html', { 'collide': collide, 'rsvp': rsvp, 'has_rsvpd': has_rsvpd })


@login_required
def rsvp_create(request, collide_id):
    form = RsvpForm(request.POST, collide_id=collide_id, request=request)
    if form.is_valid():
        form.save()
    return redirect('collides_detail', collide_id=collide_id)


@login_required
def user_events(request):
    events = Event.objects.filter(creator=request.user)
    collides = Collide.objects.filter(host=request.user)
    rsvps = Rsvp.objects.filter(attendee=request.user)
    return render(request, 'profile/events.html', { 
        'events': events, 
        'collides': collides,
        'rsvps': rsvps 
    })


@login_required
def user_collides(request):
    events = Event.objects.filter(creator=request.user)
    collides = Collide.objects.filter(host=request.user)
    rsvps = Rsvp.objects.filter(attendee=request.user)
    return render(request, 'profile/collides.html', { 
        'events': events, 
        'collides': collides,
        'rsvps': rsvps 
    })


@login_required
def user_rsvps(request):
    rsvps = Rsvp.objects.filter(attendee=request.user)
    return render(request, 'profile/rsvps.html', { 'rsvps': rsvps })


def signup(request):
    error_message = ''
    if request.method == 'POST':
        form = CustomSignupForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('events_index')
        else:
            error_message = 'Invalid Sign Up - Try Again'
    form = CustomSignupForm()
    context = {'form': form, 'error_message': error_message}
    return render(request, 'registration/signup.html', context)



