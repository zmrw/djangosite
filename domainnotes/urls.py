from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('adddomain/', views.add_domain, name='adddomain'),
    path('adddomains/', views.add_domains, name='adddomain'),
    path('alldomain/', views.all_domain, name='alldomain'),
    path('upload/', views.upload_domain, name='upload'),
]