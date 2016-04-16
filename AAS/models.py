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

RecordType = (
    (0, 'income'),
    (1, 'outcome'),
)


class Actor(models.Model):
    name = models.CharField(max_length=10,unique=True,error_messages={'unique':"username has been used"})
    def __unicode__(self):
        return self.name


class User(models.Model):
    actor = models.ForeignKey(Actor, on_delete=models.CASCADE)
    status = models.IntegerField(default= 0, choices=UserStatus)
    def __unicode__(self):
        return self.actor.name

class VIPUser(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    VipID = models.IntegerField(default=88888)
    def __unicode__(self):
        return self.user.actor.name


class Record(models.Model):
    dateUpdate = models.DateTimeField('Create/Update time')
    owner = models.ForeignKey(User,on_delete=models.CASCADE)
    recordtype = models.IntegerField(choices = RecordType,default=0)
    type = models.IntegerField(choices=AccountType,default=4)
    count = models.FloatField(default= 0.0)
    def __unicode__(self):
        return str(self.dateUpdate)[:-6] +":" + self.owner.actor.name


class Income(models.Model):
    type = models.IntegerField(choices=RecordType,default=0)
    count = models.FloatField(default = 0.0)

class Outcome(models.Model):
    type = models.IntegerField(choices=RecordType,default=0)
    count = models.FloatField(default = 0.0)

class Admin(models.Model):
    actor = models.ForeignKey(Actor, on_delete=models.CASCADE)

