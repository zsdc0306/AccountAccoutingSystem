from django.shortcuts import render
from django.http import HttpResponse
from .models import *
from django.template import loader
from django.utils import timezone
import random
# Create your views here.
def index(request):
    userlist = User.objects.all()
    template = loader.get_template('index.html')
    output = {
        'userlist':userlist
    }
    return HttpResponse(template.render(output,request))
    # output = '\n'.join([user.actor.name for user in userlist])
    # return HttpResponse(output)

def viewDetail(request, username):
    actor = Actor.objects.get(name = username)
    user = User.objects.get(actor = actor)
    VIPID = None
    try:
        vips = VIPUser.objects.filter(user=user)
        for vip in vips:
            VIPID = vip.VipID
    except Exception as e:
        VIPID = None
    # recordslist = Record(owner= User(actor = Actor(name=username)))
    recordslist = Record.objects.filter(owner = user).order_by("-dateUpdate")
    template = loader.get_template('AccountDetail.html')
    status = "normal"
    for us in UserStatus:
        if user.status == us[0]:
            status = us[1]
    for record in recordslist:
        if record.type == 0:
            record.type ="income"
        else:
            record.type ="outcome"
        if record.recordtype ==0:
            record.recordtype = "traffic"
        elif record.recordtype == 1:
            record.recordtype ="lease"
        elif record.recordtype == 2:
            record.recordtype = "dailylife"
        else:
            record.recordtype = "other"
    output = {
        'username' : username,
        'recordlist' : recordslist,
        'status': status,
        'VIPID' : VIPID,

    }
    return HttpResponse(template.render(output,request))

# Recordtype: income & outcome
# AccountType:
#     (0, 'traffic'),
#     (1, 'lease'),
#     (2, 'tax'),
#     (3, 'dailylife'),
#     (4, 'other'),


def createRecord(request, ownername, count, Recordtype, AccountType):
    template = loader.get_template('AccountDetail.html')
    ownername = request["username"]
    actor = Actor.objects.get(name=ownername)
    user = User.objects.get(actor=actor)
    type = request["type"]
    record = Record(owner=user,dataUpdate= timezone.now())




# create user, status default as normal
def addAccount(request):
    username = request.POST["userName"]
    # template = loader.get_template('index.html')
    actor = Actor(name=username)
    content =""
    try:
        actor.save()
        try:
            u = User(actor=actor, status=0)
            u.save()
            content = username + " create successfully"
        except Exception as e:
            content = e.message
    except Exception as e:
        if "UNIQUE" in e.message:
            content = username + " has been registered."
        else:
            content = e.message
    return HttpResponse(content)

def upgradeAccount(request):
    VIPCode = "UPGRADEYOVIP"
    code = request.POST["VipCode"]
    username = request.POST["username"]
    vipID = random.randint(100000,999999)
    content = ""
    if code == VIPCode:
        try:
            actor = Actor.objects.get(name=username)
            user = User.objects.get(actor=actor)
            vip = VIPUser(user = user, VipID=vipID)
            vip.save()
            content = "Cong! upgrade successfully, your VIPID is: " + str(vipID)
        except Exception as e:
            content = e.message
    else:
        content = "invalid code"
    return HttpResponse(content)


def deleteRecord(request):
    pass




