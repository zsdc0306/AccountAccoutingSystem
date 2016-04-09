from django.shortcuts import render
from django.http import HttpResponse
from .models import *
from django.template import loader
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
    return HttpResponse("You are viewing the account detail of %s." % username)