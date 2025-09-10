from django.shortcuts import render, redirect
from django.http import HttpResponse,JsonResponse
import string
import random
from django.core.mail import send_mail

from .forms import RegisterForm, LoginForm
from .models import SendEmail
from django.views.decorators.http import require_http_methods
from django.contrib.auth import get_user_model, login,logout
from django.contrib.auth.models import User

User=get_user_model()

# Create your views here.
@require_http_methods(['GET', 'POST'])
def BlogLogin(request):
    if request.method == 'GET':
        return render(request, 'login.html')
    else:
        form = LoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data.get('email')
            password = form.cleaned_data.get('password')
            remember = form.cleaned_data.get('remember')
            user = User.objects.filter(email=email).first()
            if user and user.check_password(password):
                # 登录
                login(request, user)
                # 判断是否需要记住我
                if not remember:
                    # 如果没有点击记住我，那么就要设置过期时间为0，即浏览器关闭后就会过期
                    request.session.set_expiry(0)
                # 如果点击了，那么就什么都不做，使用默认的2周的过期时间
                return redirect('/')
            else:
                print('邮箱或密码错误！')
                # form.add_error('email', '邮箱或者密码错误！')
                return render(request, 'login.html', context={"form": form})

def BlogLogout(request):
    logout(request)
    return render(request, 'index.html')


@require_http_methods(['GET','POST'])
def register(request):
    if request.method == 'GET':
        return render(request, template_name='register.html')
    else:
        form = RegisterForm(request.POST)
        if form.is_valid():
            username=form.cleaned_data.get('username')
            email = form.cleaned_data.get('email')
            password = form.cleaned_data.get('password')

            User.objects.create_user(email=email,password=password,username=username)

            # return redirect(reverse("system:login"))
            return render(request, template_name='login.html')#建议使用
        else:
            print(form.errors)
            # return redirect(reverse("system:register"))
            return render(request, template_name='register.html',context={'form':form})#建议使用

def send_email(request):
    #？email=xxx
    email=request.GET.get('email')
    if not email:
        return JsonResponse({'error':'400','message':'必须传递邮箱！'})

    #生成验证码 取四位随机阿拉伯数字
    code="".join(random.sample(string.digits,k=4))
    print(code)
    SendEmail.objects.update_or_create(email=email,defaults={'code':code})
    #这里使用同步消息传递，使用异步进程会更好
    send_mail("周世安博客验证码欢迎你！", message=f'你的注册验证码为：{code}', recipient_list=[email], from_email=None)
    return JsonResponse({'code':'200','message':'邮箱发送成功！'})

