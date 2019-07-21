[![](https://img.shields.io/badge/python-3.6.3-orange.svg)](https://www.python.org/downloads/release/python-363/)
[![](https://img.shields.io/badge/django-2.1.8-green.svg)](https://docs.djangoproject.com/en/2.1/releases/2.1/)
[![](https://img.shields.io/badge/jQuery-3.3.1-blue.svg)](https://code.jquery.com/jquery-3.3.1.min.js/)

# Django搭建注册登录功能项目

基于Django的基础学习做了一个简单的注册登录功能网站，主要搭建了3个网页（首页、注册页面、登录页面）来做一个基础的模型。注册登录界面实现刷新图片右缩form表单在左边。
<br>
<br>
1、新建一个base模板页面来作为三个页面的模板，使用Django模板继承标签实现
<br>
<br>
2、建立模型型实现简单注册登录功能的两个字段：用户名和密码（同步数据库）
<br>
<br>
3、视图函数与对应路由的编写（包括注册、登录、首页主要功能显示，后续功能实现优化了登录校验装饰器实现、注册登录密码加密、前端ajax和后端用户名重复校验、cookie和session的下发校验及删除实现用户及网站的安全性）
<br>
<br>

**首页截图**

![首页](https://github.com/py304/LoginWork/blob/master/images/showindex.jpg)
-----------
<br>

**视图代码部分截图**

![视图](https://github.com/py304/LoginWork/blob/master/images/view.jpg)
-----------
<br>

**登录页面截图**

![登录](https://github.com/py304/LoginWork/blob/master/images/showlogin.jpg)
-----------
<br>

**注册页面截图**

![注册](https://github.com/py304/LoginWork/blob/master/images/showzc.jpg)
-----------
<br>

**ajax用户名校验截图**

![ajax](https://github.com/py304/LoginWork/blob/master/images/ajax.jpg)
-----------
<br>

**视图函数完整代码展示**
```python
from django.shortcuts import render,render_to_response
from LoginApp.models import LoginUser # 导入数据模型类
from django.http import HttpResponseRedirect,JsonResponse
# 封装一个装饰器，登录校验，将index源代码放入装饰器中
def LoginValid(fun):
    def inner(request,*args,**kwargs):
        data = request.COOKIES
        cookie_user = data.get("username")
        session_user = request.session.get("username")
        if cookie_user and session_user:
            user = userValid(cookie_user)
            if user and cookie_user == session_user:
                return fun(request,*args,**kwargs)
        return HttpResponseRedirect('/login/')
    return inner

# 首页视图函数
# 新增校验功能
@LoginValid
def index(request):
    return render_to_response("index.html",locals())

# 注册视图函数
def register(request):
    # 定义一个保存状态的存储变量
    result = {"status":0,"data":""} # 默认状态0错误，数据为空；1为成功状态
    # 判断请求方式
    if request.method == "POST":
        # 获取账户输入框数据
        username = request.POST.get("username")
        # 获取密码输入框数据
        password = request.POST.get("password")
        # 判断数据是否为空
        if username and password:
            user = userValid(username)
            # 判断用户名是否重复
            if user: #用户存在
                result["data"] = "用户名重复"
            else:
                user = LoginUser() # 实例化模型类
                user.username = username
                user.password = setPassword(password)
                user.save() # 保存至数据库
                result["status"] = 1
                result["data"] = "用户注册成功"
                return HttpResponseRedirect('/login/')
        else:
            result["data"] = "用户名或密码不可以为空"
    # else:
    #     #     res["data"] = "请求方式有误"

    return render(request,"register.html",locals())

# 登录视图函数
def login(request):
    # 定义一个保存状态的存储变量
    result = {"status": 0, "data": ""}  # 默认状态0错误，数据为空；1为成功状态
    # 判断请求方式
    if request.method == "POST":
        # 获取账户输入框数据
        username = request.POST.get("username")
        # 获取密码输入框数据
        password = request.POST.get("password")
        # 判断数据是否为空
        if username:
            user = userValid(username)
            if user:#用户存在
                if user.password == setPassword(password):# 密码验证成功
                    # 密码验证成功，则设置cookie和session,并跳转index页面
                    response = HttpResponseRedirect('/index/')
                    response.set_cookie("username" , user.username)
                    request.session["username"] = user.username
                    return response
                else:
                    result["data"] = "密码错误"
            else:
                result["data"] = "用户名不存在"
        else:
            result["data"] = "用户名或密码不可以为空"
    return render(request,"login.html",locals())


# 退出功能
def exit(request):
    # username = request.COOKIES.get("username")
    response = HttpResponseRedirect('/login/')
    response.delete_cookie("username")
    del request.session["username"]
    return response

import hashlib  # 导入加密模块
# 密码加密
def setPassword(password):
    md5 = hashlib.md5()  # 创建一个hash对象，使用hashlib中的md5加密方法
    md5.update(password.encode())  # 填充要加密的数据，此处必须编码成字节，否则报错
    return md5.hexdigest()  # 返回加密的结果

# 用户名后端校验代码整合
def userValid(username):
    user = LoginUser.objects.filter(username=username).first()
    return user

# 用户名前端ajax校验
def ajax_userValid(request):
    result = {"status":0,"data":""}
    username = request.POST.get("username")
    if username:
        user = userValid(username)
        if user:
            result["data"] = "用户名已存在"
        else:
            result["status"] = 1
            result["data"] = "用户名可以使用"
    else:
        result["data"] = "用户名不能为空"
    return JsonResponse(result)



```




