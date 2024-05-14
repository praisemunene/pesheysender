"""
URL configuration for pesheysms project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    # path('admin/', admin.site.urls),
    path('',views.index, name="index" ),
    path('404',views.error, name="404" ),
    path('settings',views.changepassword, name="settings" ),
    path('creategroup',views.creategroup, name="creategroup" ),
    path('failapi',views.failapi, name="failapi" ),
    path('forgotpassword',views.forgotpassword, name="forgotpassword" ),
    path('login',views.login, name="login" ),
    path('managegroup',views.managegroup, name="managegroup" ),
    path('misreport',views.misreport, name="misreport" ),
    path('pay',views.pay, name="pay" ),
    path('register',views.register, name="register" ),
    path('senderid',views.senderid, name="senderid" ),
    path('sendsms',views.sendsms, name="sendsms" ),
    path('smspersonalised',views.smspersonalised, name="smspersonalised" ),
    path('smsstatus',views.smsstatus, name="smsstatus" ),
    path('templates',views.templates, name="templates" ),
    path('ussd/',views.ussd, name="ussd/"),
    path('registration/', views.registration, name='registration'),
    path('loginform/', views.loginform, name='loginform'),
    path('logout', views.logout, name='logout'),
    path('uploadgroup/', views.uploadcsv, name='uploadgroup'),
    path('getcontacts/', views.getcontacts, name='getcontacts'),
    path('managecontacts/', views.managecontacts, name='managecontacts'),
    path('managemycontacts/', views.managemycontacts, name='managemycontacts'),
    path('getconstcontacts/', views.getconstcontacts, name='getconstcontacts'),
    path('getwardcontacts/', views.getwardcontacts, name='getwardcontacts'),
    path('getpollingcontacts/', views.getpollingcontacts, name='getpollingcontacts'),
    path('manageconstcontacts/', views.manageconstcontacts, name='manageconstcontacts'),
    path('managewardcontacts/', views.managewardcontacts, name='managewardcontacts'),
    path('managepollingcontacts/', views.managepollingcontacts, name='managepollingcontacts'),
    path('getuserdata', views.getuserdata, name='getuserdata'),
    path('submitsms', views.submitsms, name='submitsms'),
    path('paympesa', views.paympesa, name='paympesa'),
    path('verifyemail/', views.verifyemail, name='verifyemail'),
    path('emailverification', views.emailverification, name='emailverification'),
    path('changemypassword', views.changemypassword, name='changepassword'),
    path('applysenderid', views.applysenderid, name='applysenderid'),
    path('getsenderids', views.getsenderids, name='getsenderids'),
    path('invoice', views.invoice, name='invoice'),
    path('updateprofile', views.updateprofile, name='updateprofile'),
    path('getnotifications', views.getnotifications, name='getnotifications'),
    path('admin/dashboard', views.admindashboard, name='admin/dashboard'),
    path('admin/mydashboard', views.nav, name='admin/mydashboard'),
    path('admin/sendnotification', views.sendnotification, name='admin/sendnotification'),
    path('admin/myprofile', views.myprofile, name='admin/myprofile'),
    path('admin/createusers', views.createusers, name='admin/createusers'),
    path('admin/updateusers', views.updateusers, name='admin/updateusers'),
    path('admin/createresellers', views.createresellers, name='admin/createresellers'),
    path('admin/updateresellers', views.updateresellers, name='admin/updateresellers'),
    path('admin/senderids', views.senderids, name='admin/senderids'),
    path('admin/requesttemplates', views.requesttemplates, name='admin/requesttemplates'),
    path('admin/misreports', views.misreports, name='admin/misreports'),
    path('admin/creditshistory', views.creditshistory, name='admin/creditshistory'),
    path('admin/adminlogin', views.adminlogin, name='admin/adminlogin'),
    path('admin/logout', views.admminlogout, name='admin/logout'),
    path('admin/creditassingmentusers', views.creditassingmentusers, name='admin/creditassingmentusers'),
    path('admin/creditassingmentreseller', views.creditassingmentreseller, name='admin/creditassingmentreseller'),
    path('admin/postnewuser', views.postnewuser, name='admin/postnewuser'),
    path('admin/login', views.adminlogin, name='admin/login'),
    path('get-user-details/', views.get_user_details, name='get_user_details'),
    path('get-reseller-details/', views.get_reseller_details, name='get_reseller_details'),
    path('update-reseller-details/', views.update_reseller_details, name='update_reseller_details'),
]
