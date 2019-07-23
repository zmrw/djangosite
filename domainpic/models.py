from django.db import models
from login.models import User


# Create your models here.
class DomainPicList(models.Model):
    domain = models.CharField(max_length=128, unique=True)
    # 是否截图
    hasDo = models.BooleanField(default=False)
    # isXinPeng = models.BooleanField(default=False)
    domainOwner = models.ForeignKey(User, on_delete=models.CASCADE)
    domainExpireDate = models.DateField()


class DomainPic(models.Model):
    # 域名后缀
    domainSuffix = (
        ('be', "be"),
        ('nl', "nl"),
        ('coza', "coza"),
        ('it', "it"),
        ('eu', "eu"),
        ('in', "in"),
        ('ch', "ch"),
    )
    # 域名后缀
    domainType = models.CharField(max_length=32, choices=domainSuffix)
    domainList = models.OneToOneField(DomainPicList, on_delete=models.CASCADE)
    domainExpireDate = models.DateTimeField()
    domainHistory = models.TextField()
    domainHistoryPic = models.CharField(max_length=128)
