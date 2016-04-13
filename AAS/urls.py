from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^index.html$', views.index, name='index'),
    url(r'^login/(?P<username>[A-Za-z0-9]+)/AccountDetail.html$', views.viewDetail, name= "AccountDetail"),
    # url(r'^create/(?P<username>[A-Za-z0-9]+)/$', views.addAccount, name= "addAccount"),
    url(r'^addAccount/submit/',views.addAccount,name="addAccount"),
    url(r'^form/submit/', views.upgradeAccount, name="upgradeAccount"),
    url(r'^form/delete/', views.deleteRecord, name="deleteRecord"),
]