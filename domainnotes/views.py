from django.shortcuts import render, redirect
from . import models
from .models import User, DomainList
import os


# Create your views here.
def index(request):
    if not request.session.get('is_login', None):
        return redirect('/login/')
    user_id = request.session.get('user_id')
    user = User.objects.get(id=user_id)
    domaincount = DomainList.objects.filter(domainOwner=user).count()
    hasdodomaincount = DomainList.objects.filter(domainOwner=user).filter(hasDo=True).count()
    notdodomaincount = DomainList.objects.filter(domainOwner=user).filter(hasDo=False).count()
    return render(request, 'domainnotes/index.html', locals())


def upload_domain(request):
    if not request.session.get('is_login', None):
        return redirect('/login/')
    if request.method == "POST":  # 请求方法为POST时，进行处理
        myFile = request.FILES.get("myfile", None)  # 获取上传的文件，如果没有文件，则默认为None
        if not myFile:
            message1 = '文件上传失败，请重新上传文件'
            return render(request, 'domainnotes/add-domain.html', locals())
        BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        destination_file = os.path.join(BASE_DIR, 'domainpic\\upload\\')
        destination = open(os.path.join(destination_file, myFile.name), 'wb+')  # 打开特定的文件进行二进制的写操作
        for chunk in myFile.chunks():  # 分块写入文件
            destination.write(chunk)
        destination.close()
        myFileName = os.path.join(BASE_DIR, 'domainnotes\\upload\\')
        myFileName = myFileName + myFile.name
        user_id = request.session.get('user_id')
        user = User.objects.get(id=user_id)
        with open(myFileName, 'r', encoding='utf-8') as f:
            picdomains = f.readlines()
            for picdomain in picdomains:
                picdomain = picdomain.strip('\n')
                same_domain = models.DomainList.objects.filter(domain=picdomain)
                if same_domain:
                    continue
                domainpiclist = DomainList(domain=picdomain, domainOwner=user)
                domainpiclist.save()
        message1 = '文件上传成功'
        return render(request, 'domainnotes/add-domain.html', locals())
    return render(request, 'domainnotes/add-domain.html')


def add_domain(request):
    if not request.session.get('is_login', None):
        return redirect('/login/')
    if request.method == "POST":
        domain = request.POST.get('domain')
        same_domain = models.DomainList.objects.filter(domain=domain)
        if same_domain:
            message = '域名已经存在'
            return render(request, 'domainnotes/add-domain.html', locals())
        user_id = request.session.get('user_id')
        user = User.objects.get(id=user_id)
        domainlist = models.DomainList(domain=domain, domainOwner=user)
        domainlist.save()
        message = '添加域名成功！'
        return render(request, 'domainnotes/add-domain.html', locals())
    return render(request, 'domainnotes/add-domain.html')


def add_domains(request):
    if not request.session.get('is_login', None):
        return redirect('/login/')
    user_id = request.session.get('user_id')
    user = User.objects.get(id=user_id)
    if request.method == "POST":
        domains = request.POST.get('domains')
        domains = domains.split('\n')
        for domain in domains:
            same_domain = models.DomainList.objects.filter(domain=domain)
            print(same_domain)
            if same_domain:
                continue
            else:
                domainlist = models.DomainList(domain=domain, domainOwner=user)
                domainlist.save()
            message2 = '添加域名成功！'
        return render(request, 'domainnotes/add-domain.html', locals())
    return render(request, 'domainnotes/add-domain.html')


def all_domain(request):
    if not request.session.get('is_login', None):
        return redirect('/login/')
    user_id = request.session.get('user_id')
    user = User.objects.get(id=user_id)
    domainlists = DomainList.objects.all().filter(domainOwner=user)
    return render(request, 'domainnotes/all-domain.html', locals())
