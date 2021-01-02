from django.db import models
from account.models import Account

# Create your models here.
class Activity(models.Model):
    user = models.ForeignKey(Account, on_delete=models.CASCADE)
    start_time = models.DateField()
    duration = models.TimeField()
    distance = models.FloatField(default=0)
    pace = models.FloatField(default=0)
    caption = models.CharField(max_length=1024)
    image_url = models.CharField(max_length=2048, default='http://superrace.herokuapp.com/getimage/activity/anh.png')


    def __str__(self):
        return self.user.username + '_' + self.start_time.strftime('%Y%m%d')
    def to_object(self):
        return {'start_time': self.start_time.strftime('%Y-%m-%d'),
                'duration': self.duration.strftime('%H:%M:%S'),
                'distance': self.distance,
                'pace': self.pace,
                'caption': self.caption,
                'image_url': self.image_url}