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


