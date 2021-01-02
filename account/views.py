from django.shortcuts import render
from django.http import HttpRequest, HttpResponse, HttpResponseRedirect
from .models import Account
from django.contrib.auth import authenticate, login
import random
from django.core.mail import send_mail
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import login as user_login
from django.contrib.auth.forms import AuthenticationForm
from datetime import datetime
import base64

import json

# Create your views here.


def register(request):
    data = {'success': False}
    if (request.method == 'POST'):
        username = request.POST['username']
        email = request.POST['email']
        user = Account.objects.filter(username=username)
        if (len(user) > 0):
            data = {'success': False,
                    'message': 'Username already exists.'}
            return HttpResponse(json.dumps(data), content_type='application/json')

        user = Account.objects.filter(email=email)
        if (len(user) > 0):
            data = {'success': False,
                    'message': 'Email already exists.'}
            return HttpResponse(json.dumps(data), content_type='application/json')

        password = request.POST['password']
        firstName = request.POST['first_name']
        lastName = request.POST['last_name']
        dob = request.POST['dob']
        if ('weight' in request.POST):
            weight = float(request.POST['weight'])
        else:
            weight = 0
        if ('height' in request.POST):
            height = float(request.POST['height'])
        else:
            height = 0
        if (request.POST['gender'] == 'True'):
            gender = True
        else:
            gender = False
        newAccount = Account.objects.create_user(username=username, email=email, password=password,
                                                 first_name=firstName, last_name=lastName, dob=dob, gender=gender,
                                                 weight=weight, height=height)
        if (newAccount is not None):
            data['success'] = True
    else:
        data['message'] = 'method not supported'
    return HttpResponse(json.dumps(data), content_type='application/json')


def login(request):
    data = {'success': False}
    if request.method == 'POST':
        login_form = AuthenticationForm(request, request.POST)
        if login_form.is_valid():
            user_login(request, login_form.get_user())
            data['success'] = True
    else:
        data['message'] = 'method not supported'
    return HttpResponse(json.dumps(data), content_type='application/json')


def forgot_password(request):
    data = {'success': False}
    if (request.method == 'POST'):
        email = request.POST['emaill']
        chars = 'abcdefghiklmnopqrstuvwxyz1234567890ABCDEFGHIKLMNOPQRSTUVWXYZ'
        password = ''
        for i in range(0, 8):
            password += random.choice(chars)
        f = open('staticfiles/text/hello.txt', 'w')
        f.write(email)
        f.close()

        user = Account.objects.filter(email=email)
        if (len(user) == 0):
            data['message'] = 'email does not exist'
            return HttpResponse(json.dumps(data), content_type='application/json')

        user = Account.objects.get(email=email)
        username = user.username
        user.set_password(password)
        user.save()
        send_mail(
            subject='[LLP Health] Reset password',
            message='Dear {},\n\nYour password has been changed to: {}\nLog in with this new password and then change to another.\n\nBest regards.'.format(
                username, password),
            recipient_list=[email],
            from_email='ltt.lop9a1.lhlinh@gmail.com',
        )
        data['success'] = True
    else:
        data['message'] = 'method not supported'
    return HttpResponse(json.dumps(data), content_type='application/json')


def change_password(request):
    data = {'success': False}
    if (request.method == 'POST'):
        username = request.POST['username']
        old_password = request.POST['old_password']
        new_password = request.POST['new_password']
        user = Account.objects.get(username=username)
        if (user.check_password(old_password)):
            user.set_password(new_password)
            data['success'] = True
            user.save()
        else:
            data['message'] = 'wrong password'
    else:
        data['message'] = 'method not supported'
    return HttpResponse(json.dumps(data), content_type='application/json')


def getUser(request, username):
    data = {'success': False}
    if(request.method == 'GET'):
        user = Account.objects.filter(username=username)
        if (len(user) == 0):
            data['message'] = 'This user does not exists.'
            return HttpResponse(json.dumps(data), content_type='application/json')

        user = Account.objects.get(username=username)
        data['First name'] = user.first_name
        data['Last name'] = user.last_name
        data['Email'] = user.email
        data['D.O.B'] = user.dob.strftime('%Y-%m-%d')
        data['Height'] = user.height
        data['Weight'] = user.weight
        if user.gender:
            data['Gender'] = 'Male'
        else:
            data['Gender'] = 'Female'
        data['success'] = True
    else:
        data['message'] = 'method not supported'
    return HttpResponse(json.dumps(data), content_type='application/json')

# 0supported_extension = ['jpg', 'jpeg', 'bmp', 'svg', 'png']


def avatar2(request):
    data = {'success': False}
    if (request.method == 'POST'):
        username = request.POST['username']
        filename = handle_base64_str(request.POST['image'], username)
        data['success'] = True
        return HttpResponse(json.dumps(data), content_type='application/json')
    else:
        return HttpResponse('method not supported')


def handle_base64_str(imgstring, filename):
    imgdata = base64.b64decode(imgstring)
    with open('staticfiles/avatar/'+filename+'.png', 'wb+') as destination:
        destination.write(imgdata)
    return filename


def getavatar(request, filename):
    if (request.method == 'GET'):
        with open('staticfiles/avatar/%s' % (filename), "rb") as f:
            return HttpResponse(f.read(), content_type="image/jpeg")
    else:
        return HttpResponse('method not supported')
