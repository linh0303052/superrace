from django.db import models
from account.models import Account
from event.models import Event

# Create your models here.
class JoinEvent(models.Model):
    user = models.ForeignKey(Account, on_delete=models.CASCADE, related_query_name='back_user')
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_query_name='back_event')
    date_join = models.DateField(auto_now=True)
    is_left = models.BooleanField(default=False)
    date_left = models.DateField(auto_now=True)
    distance = models.FloatField(default=0)

    def __str__(self):
        return self.user.username + '_' + self.event.title