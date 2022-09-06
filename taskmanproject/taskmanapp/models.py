from binascii import Incomplete
from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class UserTask(models.Model):
    COMPLETE = 1
    INCOMPLETE = 2
    USER_TASK_STATUS = [
        (COMPLETE, 'complete'),
        (INCOMPLETE, 'incomplete')
        
    ]
    # mark = models.BooleanField(default='No', null=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    task_name = models.CharField(max_length=100, null=True, blank=True)
    created = models.DateTimeField(default=timezone.now)
    deadline = models.CharField(max_length=100, null=True, blank=True)
    # time = self.time.strftime('%a %H:%M  %d/%m/%y')
    added_on = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    updated_on = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    status = models.PositiveSmallIntegerField(choices=USER_TASK_STATUS, default=INCOMPLETE)

    def __str__(self):
        return self.task_name


class Activity(models.Model):
    user = models.ForeignKey(User, null=True, blank=True, on_delete=models.CASCADE)
    user_task = models.CharField(max_length=100, null=True, blank=True)
    operation = models.CharField(max_length=100, null=True, blank=True)
    added_on = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    updated_on = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    
    def __str(self):
        return self.user_task + " - " + self.operation



