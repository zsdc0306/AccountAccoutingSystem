from django.shortcuts import render
from django.http import HttpResponse
from .models import *
from django.template import loader
from django.utils import timezone
import random
import matplotlib.pyplot as plt
import csv

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
        if record.recordtype == 0:
            record.recordtype ="income"
        else:
            record.recordtype ="outcome"
        if record.type ==0:
            record.type = "traffic"
        elif record.type == 1:
            record.type ="lease"
        elif record.type == 2:
            record.type = "dailylife"
        else:
            record.type = "other"
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


def createRecord(request):
    template = loader.get_template('AccountDetail.html')
    ownername = request.POST["username"]
    type = request.POST["type"]
    recordType = request.POST["recordtype"]
    actor = Actor.objects.get(name=ownername)
    user = User.objects.get(actor=actor)
    count = request.POST["recordCount"]
    dateUpdate = request.POST["dateUpdate"]
    record = Record(owner=user,dateUpdate= dateUpdate,type = type,recordtype=recordType, count=count)
    try:
        record.save()
        content = "record create successfully"
    except Exception as e:
        content = e.message
    return HttpResponse(content)

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


def actionRecord(request):
    pass

def deleteRecord(request):
    recordID = request.POST["deleterecordID"]
    target = Record.objects.get(id = recordID)
    try:
        target.delete()
        content = "delete successfully"
    except Exception as e:
        content = e.message
    return HttpResponse(content)

def updateRecord(request):
    recordID = request.POST["recordid"]
    type = request.POST["type"]
    recordType = request.POST["recordtype"]
    count = request.POST["recordCount"]
    dateUpdate = request.POST["dateUpdate"]
    target = Record.objects.get(id = recordID)
    target.type=type
    target.recordtype = recordType
    target.count = count
    target.dateUpdate = dateUpdate
    try:
        target.save()
        content = "update successfully"
    except Exception as e:
        content = e.message
    return HttpResponse(content)

def exportCSV(request):
    username = request.POST["exportrecordname"]
    actor = Actor.objects.get(name=username)
    user = User.objects.get(actor=actor)
    recordslist = Record.objects.filter(owner=user).order_by("-dateUpdate")
    contentlist = []
    content = []
    for record in recordslist:
        if record.recordtype == 0:
            record.recordtype = "income"
        else:
            record.recordtype = "outcome"
        if record.type == 0:
            record.type = "traffic"
        elif record.type == 1:
            record.type = "lease"
        elif record.type == 2:
            record.type = "dailylife"
        else:
            record.type = "other"
        content=[record.dateUpdate,record.owner,record.recordtype, record.type, record.count]
        contentlist.append(content)
    csvfile = file('userrecord.csv', 'wb')
    writer = csv.writer(csvfile)
    header = ['Date','user','income/outcome','type','count']
    writer.writerow(header)
    i = 0
    length = len(contentlist)
    for i in range(length):
        data = contentlist[i]
        writer.writerow(data)
        i += 1
    csvfile.close()
    try:
        content = open("userrecord.csv", "rb").read()
    except EOFError as e:
        content = e.message
    except Exception as e:
        content = e.message
    return HttpResponse(content, content_type="text/csv")


def genChart(request):
    username = request.POST["chartrecordname"]
    actor = Actor.objects.get(name=username)
    user = User.objects.get(actor=actor)
    recordslist = Record.objects.filter(owner=user).order_by("-dateUpdate")
    total_count = {
        0: 0.0,
        1: 0.0,
        2: 0.0,
        3: 0.0,
        4: 0.0
    }
    for record in recordslist:
        if record.recordtype == 0:
            continue
        else:
            total_count[record.type] += record.count
    traffic = total_count[0]
    lease = total_count[1]
    tax = total_count[2]
    dailylife = total_count[3]
    other = total_count[4]
    rate = [traffic, lease, tax, dailylife, other]
    colors = ['b', 'g', 'r', 'y', 'c']
    labels = ['Traffic', 'Lease', 'Tax', 'Dailylife', 'Other']
    plt.pie(rate, colors=colors, labels=labels, autopct='%d%%')
    font = {'fontsize': 30, 'verticalalignment': 'bottom', 'horizontalalignment': 'center'}
    plt.title('Record', fontdict=font)
    plt.savefig('chart.png', format='png')
    try:
        content = open("chart.png", "rb").read()
    except EOFError as e:
        content = e.message
    except Exception as e:
        content = e.message
    return HttpResponse(content, content_type ="image/png")
