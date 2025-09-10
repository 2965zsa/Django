from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.http.response import JsonResponse
from django.shortcuts import render
from django.views.decorators.http import require_http_methods, require_POST, require_GET

from .models import Categote,BlogCommit,BlogContent
from .forms import BlogContentForm

# Create your views here.
def index(request):
    blogs=BlogContent.objects.all()
    return render(request, template_name='index.html',context={'blogs':blogs})


def blog_detail(request,blog_id):
    try:
        blog=BlogContent.objects.get(pk=blog_id)
    except Exception as e:
        blog=None

    return render(request, template_name='blog_detail.html',context={'blog':blog})

@require_POST
def blog_commit(request,blog_id):
    blog_id=request.POST.get('blog_id')
    content = request.POST.get('content')
    commit=BlogCommit.objects.create(blog_id=blog_id,content=content,author=request.user)
    return render(request, template_name='blog_detail.html',context={'commit':commit})


@require_http_methods(['GET', 'POST'])
@login_required(login_url='/system/login')
def pub_blog(request):
    if request.method == 'GET':
        categories=Categote.objects.all()
        return render(request, template_name='pub_blog.html',context={'categories':categories})

    else:
        form=BlogContentForm(request.POST)
        if form.is_valid():
            title=form.cleaned_data.get('title')
            content=form.cleaned_data.get('content')
            category_id=form.cleaned_data.get('category')
            blog=BlogContent.objects.create(title=title, content=content, category_id=category_id, user=request.user)
            return JsonResponse({"code":200,"message":"success","data":{'blog_id':blog.id}})
        else:
            print(form.errors)
            return JsonResponse({"code":400,"message":"参数错误！"})

@require_GET
def search(request):
    q=request.GET.get('q')
    blogs=BlogContent.objects.filter(Q(title__icontains=q)|Q(content__icontains=q))
    return render(request,'index.html',context={'blogs':blogs})

