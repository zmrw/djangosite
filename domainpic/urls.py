from django.urls import path,re_path

from . import views

urlpatterns = [
    # path('adddomain/', views.add_domain, name='adddomain'),
    path('', views.index, name='index'),
    path('uploadpicdomain/', views.upload_domain, name='upload'),
    path('allpicdomain/', views.all_domain, name='allpicdomain'),
    path('getpic/', views.getpic, name='getpic'),
    # path('showdatepicdomain/', views.show_date_domainpic, name='getpic'),
    re_path('date/(?P<date>[1-9]\d{3}-(0[1-9]|1[0-2])-(0[1-9]|[1-2][0-9]|3[0-1]))/$', views.get_domainpic_by_date,
         name='show_goods_detil'),
    re_path('getdateallpic/(?P<date>[1-9]\d{3}-(0[1-9]|1[0-2])-(0[1-9]|[1-2][0-9]|3[0-1]))/$', views.get_date_allpic,
         name='show_goods_detil'),
    re_path('showdatepicdomain/(?P<date>[1-9]\d{3}-(0[1-9]|1[0-2])-(0[1-9]|[1-2][0-9]|3[0-1]))/$', views.show_date_domainpic,
         name='show_goods_detil'),
    re_path('showdatepicdomainold/(?P<date>[1-9]\d{3}-(0[1-9]|1[0-2])-(0[1-9]|[1-2][0-9]|3[0-1]))/$', views.show_date_domainpic_old_tem,
         name='show_goods_detil'),
]
