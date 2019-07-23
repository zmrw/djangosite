from django.shortcuts import render, redirect
from . import models
from .models import DomainPicList, DomainPic, User
import os
import datetime
from selenium import webdriver
from selenium.webdriver.chrome.options import Options


def to_datetime(text):
    """字符串转时间"""
    if not text:
        return None

    # 定义字典根据时间字符串匹配不同的格式
    time_dict = {
        1: "%Y-%m-%d %H:%M:%S.%f",
        2: "%Y-%m-%d %H:%M",
        3: "%Y-%m-%d %H:%M:%S",
    }
    # 如果中间含有时间部分就用：判断
    try:
        if str(text).find('.') > -1:
            return datetime.datetime.strptime(text, time_dict[1])
        elif ':' in text:
            time_list = text.split(':')
            return datetime.datetime.strptime(text, time_dict[len(time_list)])
        else:
            return datetime.datetime.strptime(text, "%Y-%m-%d")
    except:
        return None


def to_date(text):
    """字符串转日期"""
    d = to_datetime(text)
    if d:
        return d.date()


# Create your views here.
# def add_domain(request):
#     if not request.session.get('is_login', None):
#         return redirect('/login/')
#     if request.method == "POST":
#         domain = request.POST.get('domain')
#         same_domain = models.DomainPicList.objects.filter(domain=domain)
#         if same_domain:
#             message = '域名已经存在'
#             return render(request, 'domainnotes/add-pic-domain.html', locals())
#         user_id = request.session.get('user_id')
#         user = User.objects.get(id=user_id)
#         domainlist = models.DomainPicList(domain=domain, domainOwner=user)
#         domainlist.save()
#         message = '添加域名成功！'
#         return render(request, 'domainnotes/add-pic-domain.html', locals())
#     return render(request, 'domainnotes/add-pic-domain.html')

def index(request):
    pass


def upload_domain(request):
    if not request.session.get('is_login', None):
        return redirect('/login/')
    if request.method == "POST":  # 请求方法为POST时，进行处理
        myFile = request.FILES.get("myfile", None)  # 获取上传的文件，如果没有文件，则默认为None
        if not myFile:
            message1 = '文件上传失败，请重新上传文件'
            return render(request, 'domainnotes/add-pic-domain.html', locals())
        BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        destination_file = os.path.join(BASE_DIR, 'domainpic\\upload\\')
        destination = open(os.path.join(destination_file, myFile.name), 'wb+')  # 打开特定的文件进行二进制的写操作
        for chunk in myFile.chunks():  # 分块写入文件
            destination.write(chunk)
        destination.close()
        domainpicdate = to_date(myFile.name)
        myFileName = os.path.join(BASE_DIR, 'domainpic\\upload\\')
        myFileName = myFileName + myFile.name
        user_id = request.session.get('user_id')
        user = User.objects.get(id=user_id)
        with open(myFileName, 'r', encoding='utf-8') as f:
            picdomains = f.readlines()
            for picdomain in picdomains:
                picdomain = picdomain.strip('\n')
                same_domain = models.DomainPicList.objects.filter(domain=picdomain)
                if same_domain:
                    continue
                domainpiclist = DomainPicList(domain=picdomain, domainOwner=user, domainExpireDate=domainpicdate)
                domainpiclist.save()
        message1 = '文件上传成功'
        domainpiclist = DomainPicList.objects.values('domainExpireDate').distinct().order_by('-domainExpireDate')
        return render(request, 'domainnotes/add-pic-domain.html', locals())
    domainpiclist = DomainPicList.objects.values('domainExpireDate').distinct().order_by('-domainExpireDate')
    return render(request, 'domainnotes/add-pic-domain.html', locals())


def all_domain(request):
    if not request.session.get('is_login', None):
        return redirect('/login/')
    domainlists = DomainPicList.objects.values('domainExpireDate').distinct().order_by('-domainExpireDate')
    return render(request, 'domainnotes/all-pic-domain.html', locals())


def get_domain_pic(domain):
    domainpiclist = DomainPicList.objects.get(domain=domain)
    domainExpireDate = domainpiclist.domainExpireDate
    picname = domain + '.png'
    # domainpic = 'F:\\djangosite\\domainpic\\domainpicimage\\' + str(domainExpireDate) + '\\' + picname
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    pic_path = os.path.join(BASE_DIR, 'domainpic\static\domainpic\image\\')

    pic_path = str(pic_path) + str(domainExpireDate)
    if not os.path.exists(pic_path):
        os.mkdir(pic_path)
    else:
        pass
    chrome_options = Options()
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--log-level=3')
    browser = webdriver.Chrome(chrome_options=chrome_options)
    try:
        browser.set_page_load_timeout(100)
        url = 'https://web.archive.org/web/201905/' + domain
        browser.get(url)
        domainpic = pic_path + '\\' + picname
        browser.save_screenshot(domainpic)
        if ".nl" in domain:
            domainpic = DomainPic(domainType='nl', domainExpireDate=domainExpireDate, domainList=domainpiclist,
                                  domainHistory='ceshi', domainHistoryPic=picname)
            print(domainpic)
            domainpic.save()
            domainpiclist.hasDo = True
            domainpiclist.save()
        elif ".be" in domain:
            domainpic = DomainPic(domainType='be', domainExpireDate=domainExpireDate, domainList=domainpiclist,
                                  domainHistory='ceshi', domainHistoryPic=picname)
            domainpic.save()
            domainpiclist.hasDo = True
            domainpiclist.save()
        elif ".it" in domain:
            domainpic = DomainPic(domainType='it', domainExpireDate=domainExpireDate, domainList=domainpiclist,
                                  domainHistory='ceshi', domainHistoryPic=picname)
            domainpic.save()
            domainpiclist.hasDo = True
            domainpiclist.save()
        elif ".coza" in domain:
            domainpic = DomainPic(domainType='coza', domainExpireDate=domainExpireDate, domainList=domainpiclist,
                                  domainHistory='ceshi', domainHistoryPic=picname)
            domainpic.save()
            domainpiclist.hasDo = True
            domainpiclist.save()
        elif ".ch" in domain:
            domainpic = DomainPic(domainType='ch', domainExpireDate=domainExpireDate, domainList=domainpiclist,
                                  domainHistory='ceshi', domainHistoryPic=picname)
            domainpic.save()
            domainpiclist.hasDo = True
            domainpiclist.save()
        else:
            pass
    except Exception as e:
        print(e)
        pass


def getpic(request):
    if not request.session.get('is_login', None):
        return redirect('/login/')
    if request.method == "POST":  # 请求方法为POST时，进行处理
        domain = request.POST.get('domain')
        get_domain_pic(domain)
        message = '添加截图成功！'
        return render(request, 'domainnotes/get-pic-domain.html', locals())
    return render(request, 'domainnotes/get-pic-domain.html')


def get_domainpic_by_date(request, date):
    domainpics = DomainPicList.objects.all().filter(domainExpireDate=date)
    domainpicsnopic = DomainPicList.objects.all().filter(domainExpireDate=date).filter(hasDo=False)
    return render(request, 'domainnotes/date-pic-domain.html', locals())


def get_date_allpic(request, date):
    domainpics = DomainPicList.objects.all().filter(domainExpireDate=date).filter(hasDo=False)
    for domain in domainpics:
        print(domain.domain)
        get_domain_pic(domain.domain)
    return render(request, 'domainnotes/date-pic-domain.html', locals())


def show_date_domainpic(request, date):
    domainpics = DomainPicList.objects.all().filter(domainExpireDate=date).filter(hasDo=True)
    return render(request, 'domainnotes/show-date-domainpic.html', locals())


# 老模板展示截图
def show_date_domainpic_old_tem(request, date):
    domainpics = DomainPicList.objects.all().filter(domainExpireDate=date).filter(hasDo=True)
    return render(request, 'domainpic/index.html', locals())
