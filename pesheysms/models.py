from django.db import models

class Users(models.Model):
    firstname = models.CharField(max_length=30, blank=False, null=False)
    lastname = models.CharField(max_length=30, blank=False, null=False)
    email = models.EmailField()
    password = models.CharField(max_length=100, blank=False, null=False)
    userstatus = models.CharField(max_length=30, blank=True, null=True, default=1)
    number = models.CharField(max_length=30, blank=True, null=True)
    address = models.CharField(max_length=30, blank=True, null=True)
    vercode = models.CharField(max_length=30, blank=True, null=True)
    isverified = models.CharField(max_length=30, blank=True, null=True,  default="0")
    firmname = models.CharField(max_length=30, blank=True, null=True)
    expiredon = models.CharField(max_length=30, blank=True, null=True, default="1970-01-01 23:59:59")
    price = models.CharField(max_length=30, blank=True, null=True, default="0.3")
    usertype = models.CharField(max_length=30, blank=True, null=True)
    hideno = models.CharField(max_length=30, blank=True, null=True, default=1)
    httpapi = models.CharField(max_length=30, blank=True, null=True, default=1)
    panel = models.CharField(max_length=30, blank=True, null=True, default=1)
    mis = models.CharField(max_length=30, blank=True, null=True, default=1)
    usermode = models.CharField(max_length=30, blank=True, null=True, default="prepaid")
    showcontacts = models.CharField(max_length=30, blank=True, null=True, default="0")
    countycontact = models.CharField(max_length=30, blank=True, null=True)
    constituencycontact = models.CharField(max_length=30, blank=True, null=True)
    wardcontact = models.CharField(max_length=30, blank=True, null=True)
    pollingcontact = models.CharField(max_length=30, blank=True, null=True)

    class Meta:
        app_label = 'pesheysms'

class UploadedCSV(models.Model):
    useremail = models.EmailField()
    filename = models.CharField(max_length=255)
    customfilename = models.CharField(max_length=255)
    createdat = models.DateTimeField(auto_now_add=True)
    mobilecount = models.PositiveIntegerField()

    def __str__(self):
        return self.customfilename


class getsenderid(models.Model):
    useremail = models.EmailField()
    senderid = models.CharField(max_length=255)
    smstype = models.CharField(max_length=255)
    serviceprovider = models.CharField(max_length=255, default="safaricom")
    applicationletter = models.CharField(max_length=255)
    cr12 = models.CharField(max_length=255)
    cr13 = models.CharField(max_length=255)
    certincorp = models.CharField(max_length=255)
    bussinesscert = models.CharField(max_length=255)
    requestedon = models.CharField(max_length=255)
    approvedon = models.CharField(max_length=255)
    status = models.CharField(max_length=50, default="Pending")  

    def __str__(self):
        return self.customfilename

class reseller(models.Model):
    username = models.EmailField()
    password = models.CharField(max_length=255)
    description = models.CharField(max_length=255)
    customername = models.CharField(max_length=255)
    creditsavailableussd = models.CharField(max_length=1255, default=0)
    creditsavailablesms = models.CharField(max_length=1255, default=0)
    address = models.CharField(max_length=255)
    license = models.CharField(max_length=255)
    createsender = models.CharField(max_length=255)
    expiry = models.CharField(max_length=255)
    createdon = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    accountmanager = models.CharField(max_length=255)
    priority = models.CharField(max_length=255)
    isadmin = models.CharField(max_length=255, default=0)

    def __str__(self):
        return self.username

class Notification(models.Model):
    email = models.EmailField()
    notification = models.CharField(max_length=255)
    picture = models.CharField(max_length=255)
    time = models.CharField(max_length=255, blank=True)

    def __str__(self):
        return f"{self.email} - {self.notification} - {self.time}"