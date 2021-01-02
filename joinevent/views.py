from django.shortcuts import render
import json
from django.http import HttpRequest, HttpResponse
from .models import JoinEvent
from event.models import Event
from account.models import Account
import datetime

# Create your views here.


def join_event(request):
    data = {'success': False}
    if request.method == 'POST':
        user = Account.objects.get(username=request.POST['username'])
        event = Event.objects.get(title=request.POST['event_title'])
        je = JoinEvent.objects.filter(user=user, event=event, is_left=True)
        if len(je) > 0:
            je = je[0]
            je.is_left = False
            je.distance = 0
        else:
            je = JoinEvent(user=user, event=event)
        event.no_runners += 1
        event.save()
        je.save()
        data['success'] = True
    else:
        data['message'] = 'method not supported'
    return HttpResponse(json.dumps(data), content_type='application/json')


def leave_event(request):
    data = {'success': False}
    if request.method == 'POST':
        user = Account.objects.get(username=request.POST['username'])
        event = Event.objects.get(title=request.POST['event_title'])
        event.no_runners -= 1
        je = JoinEvent.objects.get(user=user, event=event)
        je.is_left = True
        date = datetime.datetime.now()
        je.date_left = date        
        event.total_distance -= je.distance
        event.save()
        je.save()
        data['success'] = True
    else:
        data['message'] = 'method not supported'
    return HttpResponse(json.dumps(data), content_type='application/json')