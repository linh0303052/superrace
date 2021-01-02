from django.shortcuts import render
import datetime
import base64
import json
from django.http import HttpRequest, HttpResponse
from .models import Activity
from event.models import Event
from joinevent.models import JoinEvent
from account.models import Account

# Create your views here.


def post_activity(request):
    # save activity
    data = {'success': False}
    if request.method == 'POST':
        user = Account.objects.get(username=request.POST['username'])
        start_time = datetime.datetime.now()
        duration = request.POST['duration']
        distance = float(request.POST['distance'])
        pace = float(request.POST['pace'])
        caption = request.POST['caption']
        act = Activity(user=user, start_time=start_time,
                       duration=duration, distance=distance,
                       pace=pace, caption=caption)

        # if have an image
        if 'image' in request.POST:
            image_url = handle_base64_str(
                request.POST['image'], username, start_time)
            act.image_url = image_url
        act.save()

        data['milestone_pass'] = []
        # update total distance for joining events
        events = Event.objects.filter(back_event__user=user,
                                      end_date__gte=start_time,
                                      back_event__is_left=False)
        for event in events:
            event.total_distance += distance
            jevent = JoinEvent.objects.get(user=user,
                                           event=event)
            is_pass = jevent.distance >= event.milestone
            jevent.distance += distance
            jevent.save()
            event.save()
            if jevent.distance >= event.milestone and not is_pass:
                data['milestone_pass'].append(event.title)
        data['success'] = True
    else:
        data['message'] = 'method not supported'
    return HttpResponse(json.dumps(data), content_type='application/json')


def handle_base64_str(imgstring, username, start_time):
    imgdata = base64.b64decode(imgstring)
    start_time = start_time.strftime('%Y%m%d%H%m%s')
    file_url = 'http://superrace.herokuapp.com/getimage/activity/%s%s.png' % (
        username, start_time)
    with open('staticfiles/activity/'+username+start_time+'.png', 'wb+') as destination:
        destination.write(imgdata)
    return file_url


def get_activities(request, username):
    data = {'success': False}
    if request.method == 'GET':
        user = Account.objects.get(username=username)
        activities = Activity.objects.filter(user=user).order_by('start_time')
        data['activities'] = []
        for activity in activities:
            data['activities'].append(activity.to_object())
        data['success'] = True
    else:
        data['message'] = 'method not supported'
    return HttpResponse(json.dumps(data), content_type='application/json')


def get_image(request, typee, filename):
    if (request.method == 'GET'):
        with open('staticfiles/%s/%s' % (typee, filename), "rb") as f:
            return HttpResponse(f.read(), content_type="image/jpeg")
    else:
        return HttpResponse('method not supported')


# def set_image_event(request):
#     event = Event.objects.get(title=request.POST['event_title'])
#     imgstring = request.POST['image']
#     start_time = event.start_time.strftime('%Y%m%d%H%m%s')
#     username = event.user.username
#     filename = username+start_time+'.png'
#     handle_test_image(imgstring, 'event', filename)
#     thumbail_url = "http://superrace.herokuapp.com/getimage/event/%s" % (filename)
#     event.thumbnail_url = thumbail_url
#     event.save()
#     return HttpResponse(thumbail_url)


# def handle_test_image(imgstring, typee, filename):
#     imgdata = base64.b64decode(imgstring)
#     with open('staticfiles/%s/%s' % (typee, filename), 'wb+') as destination:
#         destination.write(imgdata)