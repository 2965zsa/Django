from django import forms
from django.contrib.auth import get_user_model
from .models import SendEmail

User = get_user_model()

class RegisterForm(forms.ModelForm):
    username = forms.CharField( max_length=20,min_length=2,error_messages={
        'required':'请输入长度为2-20的名字',
        'min_length':'请输入长度为2-20的名字',
        'max_length':'请输入长度为2-20的名字',

    })

    password = forms.CharField(max_length=20,min_length=3,error_messages={
        'required':'请输入密码'
    })

    email = forms.EmailField(error_messages=
    {'required':'请输入你的qq邮箱',
     'invalid':'请输入你正确的qq邮箱',
     })

    code = forms.CharField(max_length=4,min_length=4,error_messages={
        'required':'请输入4位验证码',
        'invalid':'请输入4位验证码',
    })

    class Meta:
        model = User
        fields = ['username','email', 'password']

    def clean_email(self):
        email = self.cleaned_data.get('email')
        exists = User.objects.filter(email=email).exists()
        if exists:
            raise forms.ValidationError("邮箱已被注册！")
        else:
            return email

    def clean_code(self):
        code = self.cleaned_data.get('code')
        email = self.cleaned_data.get('email')

        send_email = SendEmail.objects.filter(code=code,email=email).first()
        if not send_email:
            raise forms.ValidationError("验证码或者邮箱不匹配！")
        else:
            send_email.delete()
            return code

class LoginForm(forms.ModelForm):
    password = forms.CharField(max_length=20, min_length=3, error_messages={
        'required': '请输入密码'
    })

    email = forms.CharField(error_messages=
    {'required': '请输入你的qq邮箱',
      'invalid': '请输入你正确的qq邮箱',
    })

    remember = forms.ImageField(required=False)

    class Meta:
        model = User
        fields = ['email', 'password']
