from django.shortcuts import render, redirect
from . import models
from .models import DomainList, DomainNotes, User, CloudflareList
import requests
import json
from django.utils import timezone


# Create your views here.
def addcloudflare(request):
    if not request.session.get('is_login', None):
        return redirect('/index/')
    user_id = request.session.get('user_id')
    user = User.objects.get(id=user_id)
    if request.method == 'POST':
        email = request.POST.get('cloudflareemail')
        api = request.POST.get('cloudflareapi')
        same_email = models.CloudflareList.objects.filter(email=email)
        if same_email:
            message = "该cloudflare账户已经存在"
            cloudflarelist = models.CloudflareList.objects.all().filter(user=user)
            return render(request, 'domainnotes/add-cloudflare.html', locals())
        else:
            cloudflarelist = models.CloudflareList(email=email, api=api, user=user)
            cloudflarelist.save()
            message = "成功添加cloudflare账户"
            cloudflarelist = models.CloudflareList.objects.all().filter(user=user)
            return render(request, 'domainnotes/add-cloudflare.html', locals())
    else:
        cloudflarelist = models.CloudflareList.objects.all().filter(user=user)
        return render(request, 'domainnotes/add-cloudflare.html', locals())


def addcloudflaredomain(request):
    if not request.session.get('is_login', None):
        return redirect('/index/')
    user_id = request.session.get('user_id')
    user = User.objects.get(id=user_id)
    if request.method == 'POST':
        vps = request.POST.get('vps')
        domain = request.POST.get('domain')
        email = request.POST.get('cloudflareemail')
        dotime = timezone.now()
        cloudflarelist = CloudflareList.objects.get(email=email)
        api = cloudflarelist.api
        hasdomain = DomainList.objects.filter(domain=domain)
        if hasdomain:
            names = ['www', domain]
            headers = {'X-Auth-Email': email,
                       'X-Auth-Key': api,
                       'Content-Type': 'application/json'}
            r = requests.get('https://api.cloudflare.com/client/v4/accounts?page=1&per_page=20&direction=desc',
                             headers=headers)
            account_id = r.json()['result'][0]['id']
            data1 = {'name': domain, 'account': {'id': account_id, 'name': email}, 'jump_start': False}
            url1 = 'https://api.cloudflare.com/client/v4/zones'
            r = requests.post(url1, headers=headers, data=json.dumps(data1))
            r_result = r.json()
            # print(r_result['success'])
            try:
                domain_id = r_result['result']['id']
            except:
                message = "请网页登陆cloudflare,删除该域名重新添加"
                cloudflarelist1 = CloudflareList.objects.all()
                return render(request, 'domainnotes/add-cloudflare-domain.html', locals())
            # 添加DNS
            for name in names:
                data2 = {'type': 'A',
                         'name': name,
                         'content': vps,
                         'ttl': 1,
                         'priority': 0,
                         'proxied': True}
                url2 = 'https://api.cloudflare.com/client/v4/zones/' + domain_id + '/dns_records'
                requests.post(url2, data=json.dumps(data2), headers=headers)

            # 修改SSL模式
            url3 = 'https://api.cloudflare.com/client/v4/zones/' + domain_id + '/settings/ssl'
            requests.patch(url3, data=json.dumps({'value': 'flexible'}), headers=headers)

            domainlist = DomainList.objects.get(domain=domain)
            domainlist.hasDo = True
            domainlist.save()
            domiannotes = DomainNotes(domainVps=vps, domainList=domainlist, domainCloudflare=email, domainDoDate=dotime)
            domiannotes.save()
            domainlist.save()
            message = '恭喜! %s 添加成功.' % domain
            return render(request, 'domainnotes/add-cloudflare-domain.html', locals())
        else:
            names = ['www', domain]
            headers = {'X-Auth-Email': email,
                       'X-Auth-Key': api,
                       'Content-Type': 'application/json'}
            r = requests.get('https://api.cloudflare.com/client/v4/accounts?page=1&per_page=20&direction=desc',
                             headers=headers)
            account_id = r.json()['result'][0]['id']
            data1 = {'name': domain, 'account': {'id': account_id, 'name': email}, 'jump_start': False}
            url1 = 'https://api.cloudflare.com/client/v4/zones'
            r = requests.post(url1, headers=headers, data=json.dumps(data1))
            r_result = r.json()
            # print(r_result['success'])
            try:
                domain_id = r_result['result']['id']
            except:
                message = "请网页登陆cloudflare,删除该域名重新添加"
                cloudflarelist1 = CloudflareList.objects.all().filter(user=user)
                return render(request, 'domainnotes/add-cloudflare-domain.html', locals())
            # 添加DNS
            for name in names:
                data2 = {'type': 'A',
                         'name': name,
                         'content': vps,
                         'ttl': 1,
                         'priority': 0,
                         'proxied': True}
                url2 = 'https://api.cloudflare.com/client/v4/zones/' + domain_id + '/dns_records'
                requests.post(url2, data=json.dumps(data2), headers=headers)

            # 修改SSL模式
            url3 = 'https://api.cloudflare.com/client/v4/zones/' + domain_id + '/settings/ssl'
            requests.patch(url3, data=json.dumps({'value': 'flexible'}), headers=headers)

            domainlist = DomainList(domain=domain, domainOwner=user, hasDo=True)
            domainlist.save()
            domiannotes = DomainNotes(domainVps=vps, domainList=domainlist, domainCloudflare=email, domainDoDate=dotime)
            domiannotes.save()
            message = '恭喜! %s 添加成功.' % domain
            return render(request, 'domainnotes/add-cloudflare-domain.html', locals())
        cloudflarelist1 = CloudflareList.objects.all().filter(user=user)
        return render(request, 'domainnotes/add-cloudflare-domain.html', locals())
    cloudflarelist1 = CloudflareList.objects.all().filter(user=user)
    return render(request, 'domainnotes/add-cloudflare-domain.html', locals())
