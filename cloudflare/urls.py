from django.urls import path

from . import views

urlpatterns = [
    path('addcloudflare/', views.addcloudflare, name='addcloudflare'),
    path('addcloudflaredomain/', views.addcloudflaredomain, name='addcloudflare'),
]
