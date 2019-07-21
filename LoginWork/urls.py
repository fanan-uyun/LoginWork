"""LoginWork URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from LoginApp.views import *

urlpatterns = [
    path('admin/', admin.site.urls),
    path('index/', index), # 首页路由
    path('register/', register), # 注册路由
    path('login/', login), # 登录路由
    path('exit/', exit), # 退出路由
    path('ajax/', ajax_userValid), # ajax前端用户名校验路由

]
