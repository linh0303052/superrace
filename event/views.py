from django.shortcuts import render
from datetime import datetime
import base64
import json
from django.http import HttpRequest, HttpResponse
from .models import Event
from joinevent.models import JoinEvent
from activity.models import Activity
from account.models import Account

# Create your views here.


def create_event(request):
    data = {'success': False}
    if request.method == 'POST':
        username = request.POST['username']
        user = Account.objects.get(username=username)
        title = request.POST['title']
        description = request.POST['description']
        start_date = request.POST['start_date']
        end_date = request.POST['end_date']
        milestone = float(request.POST['milestone'])
        event = Event(title=title, description=description,
                      user=user, start_date=start_date,
                      end_date=end_date, milestone=milestone)
        if 'thumbnail' in request.POST:
            thumbnail_url = handle_base64_str(
                request.POST['thumbnail'], username, start_date)
            event.thumbnail_url = thumbnail_url
        event.save()
        data['success'] = True
    else:
        data['message'] = 'method not supported'
    return HttpResponse(json.dumps(data), content_type='application/json')


def handle_base64_str(imgstring, username, start_date):
    imgdata = base64.b64decode(imgstring)
    start_date = start_date.strftime('%Y%m%d%H%M%S')
    file_url = 'http://superrace.herokuapp.com/getimage/event/%s%s.png' % (
        username, start_date)
    with open('staticfiles/event/'+username+start_date+'.png', 'wb+') as destination:
        destination.write(imgdata)
    return file_url


def get_event(request):
    if request.method == 'POST':
        title = request.POST['event_title']
        event = Event.objects.get(title=title)
        data = event.to_object()
        data['success'] = True
    else:
        data['success'] = False
        data['message'] = 'method not supported'
    return HttpResponse(json.dumps(data), content_type='application/json')


def get_new_event(request, username):
    data = {'success': False}
    if request.method == 'GET':
        user = Account.objects.get(username=username)
        events = Event.objects.exclude(back_event__user=user, is_deleted=False)
        data['new_events'] = []
        for event in events:
            data['new_events'].append(event.to_object())
        data['success'] = True
    else:
        data['message'] = 'method not supported'
    return HttpResponse(json.dumps(data), content_type='application/json')


def get_joined_event(request, username):
    data = {'success': False}
    if request.method == 'GET':
        user = Account.objects.get(username=username)
        events = Event.objects.filter(back_event__user=user, is_deleted=False)
        data['joined_events'] = []
        for event in events:
            data['joined_events'].append(event.to_object())
        data['success'] = True
    else:
        data['message'] = 'method not supported'
    return HttpResponse(json.dumps(data), content_type='application/json')


def get_created_events(request, username):
    data = {'success': False}
    if request.method == 'GET':
        user = Account.objects.get(username=username)
        events = Event.objects.filter(user=user, is_deleted=False)
        data['created_events'] = []
        for event in events:
            data['created_events'].append(event.to_object())
        data['success'] = True
    else:
        data['message'] = 'method not supported'
    return HttpResponse(json.dumps(data), content_type='application/json')


def delete_event(request):
    data = {'success': False}
    if request.method == 'GET':
        event = Event.objects.get(title=request.POST['even_title'])
        event.is_deleted = True
        data['success'] = True
    else:
        data['message'] = 'method not supported'
    return HttpResponse(json.dumps(data), content_type='application/json')

