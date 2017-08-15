"""LuffyAudit URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin
from audit import views

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^$', views.index),
    url(r'login.html$', views.acc_login),
    url(r'logout/$', views.acc_logout),

    url(r'hostlist.html$', views.host_list ,name="host_list"),
    url(r'^api/hostlist/$', views.get_host_list, name="get_host_list"),
    url(r'^api/start_cmd/$', views.start_cmd, name="start_cmd"),
    url(r'^api/get_token/$', views.get_token, name="get_token"),

]
