"""group5server URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from account import views as acc
from event import views as event
from activity import views as act
from joinevent import views as jevent
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

urlpatterns = [
    path('admin/', admin.site.urls),
    path('login/', acc.login),
    path('register/', acc.register),
    path('getuser/<username>/', acc.getUser),
    path('createactivity/', act.post_activity),
    path('getactivities/<username>/', act.get_activities),
    path('getimage/<typee>/<filename>/', act.get_image),
    # path('seteventimage/', act.set_image_event),
    path('joinevent/', jevent.join_event),
    path('leaveevent/', jevent.leave_event),
    path('createevent/', event.create_event),
    path('getevent/', event.get_event),
    path('deleteevent/', event.delete_event),
    path('getnewevents/<username>/', event.get_new_event),
    path('getjoinedevents/<username>/', event.get_joined_event),
    path('getcreatedevents/<username>/', event.get_created_events),
]

urlpatterns += staticfiles_urlpatterns()
