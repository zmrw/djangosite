from django.db import models
from login.models import User


# Create your models here.
class DomainList(models.Model):
    domain = models.CharField(max_length=128, unique=True)
    # 是否上站
    hasDo = models.BooleanField(default=False)
    add_time = models.DateTimeField(auto_now_add=True)
    domainOwner = models.ForeignKey(User, on_delete=models.CASCADE)


class DomainNotes(models.Model):
    # 域名后缀
    domainSuffix = (
        ('be', "be"),
        ('nl', "nl"),
        ('coza', "coza"),
    )
    # 域名后缀
    domainType = models.CharField(max_length=32, choices=domainSuffix, blank=True)
    domainList = models.OneToOneField(DomainList, on_delete=models.CASCADE)
    domainDoDate = models.DateTimeField(blank=True)
    domainVps = models.CharField(max_length=64, blank=True)
    doaminTemplate = models.CharField(max_length=64, blank=True)
    domainDb = models.CharField(max_length=64, blank=True)
    domainHistory = models.TextField(blank=True)
    domainCloudflare = models.EmailField(blank=True)
    domainWebPic = models.CharField(max_length=128, blank=True)
    domainHistoryPic = models.CharField(max_length=128, blank=True)
