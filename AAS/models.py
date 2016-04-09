from __future__ import unicode_literals

from django.db import models

# Create your models here.

ActionType = (
    (0, 'record'),
    (1, 'modify'),
    (2, 'delete'),
)
AccountType = (
    (0, 'traffic'),
    (1, 'lease'),
    (2, 'tax'),
    (3, 'dailylife'),
    (4, 'other'),
)
UserStatus = (
    (0, 'normal'),
    (1, 'banned'),
)

class actor(models.Model):
    name = models.CharField(max_length=10)
    def __str__(self):
        return self.name


class User(models.Model):
    actor = models.ForeignKey(actor, on_delete=models.CASCADE)
    status = models.IntegerField(default= 0, choices=UserStatus)
    def __str__(self):
        return self.actor.name

class VIPUser(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    VipID = models.IntegerField
    def __str__(self):
        return self.user.actor.name


class record(models.Model):
    dataUpdate = models.DateTimeField('Create/Update time')
    owner = models.ForeignKey(User,on_delete=None)
    def __str__(self):
        return self.owner.actor.name

class inCome(models.Model):
    record = models.ForeignKey(record,on_delete=models.CASCADE)
    count = models.FloatField
    type = models.IntegerField(choices=AccountType)

class outCome(models.Model):
    record = models.ForeignKey(record,on_delete=models.CASCADE)
    count = models.FloatField
    type = models.IntegerField(choices=AccountType)




