from django.db import models
from account.models import Account

# Create your models here.
class Event(models.Model):
    title = models.CharField(max_length=128)
    description = models.CharField(max_length=4096)
    user = models.ForeignKey(Account, on_delete=models.CASCADE,
                            related_query_name='back_creator', db_constraint=False)
    start_date = models.DateField()
    end_date = models.DateField()
    milestone = models.FloatField(default=0)
    thumbnail_url = models.CharField(max_length = 2048, default='http://superrace.herokuapp.com/getimage/event/anh.png')
    no_runners = models.IntegerField(default=0)
    total_distance = models.FloatField(default=0)
    is_deleted = models.BooleanField(default=False)

    def __str__(self):
        return self.title

    def to_object(self):
        return {'title': self.title,
                'description': self.description,
                'start_date': self.start_date.strftime('%Y-%m-%d'),
                'end_date': self.end_date.strftime('%Y-%m-%d'),
                'milestone': self.milestone,
                'thumbnail_url': self.thumbnail_url,
                'no_runners': self.no_runners,
                'total_distance': self.total_distance}
    