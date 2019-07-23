from django.db import models
from login.models import User
from domainnotes.models import DomainNotes, DomainList


# Create your models here.
class CloudflareList(models.Model):
    email = models.EmailField(unique=True)
    api = models.CharField(max_length=128)
    # user = models.OneToOneField(User, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    domainlist = models.ForeignKey(DomainList, on_delete=models.CASCADE,blank=True,default='123')
