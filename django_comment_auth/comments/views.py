from django.conf import settings
from django.shortcuts import render
from django.contrib.auth import authenticate,login,logout
from django.shortcuts import redirect
from django.urls import reverse

from .models import Comment

def comments_index(request):
    if not request.user.is_authenticated:
        return redirect('%s?next=%s' % (settings.LOGIN_URL, request.path))
    context = {}
    context['comments'] = Comment.objects.all()
    return render(request,'comments/index.html', context)

def comments_show(request, comment_id):
    if not request.user.is_authenticated:
        return redirect('%s?next=%s' % (settings.LOGIN_URL, request.path))
    context = {}
    context['comment_id'] = comment_id
    return render(request,'comments/show.html',context)

def comments_create(request):
    if not request.user.is_authenticated:
        return redirect('%s?next=%s' % (settings.LOGIN_URL, request.path))
    context = {}
    context['page_title'] = 'コメントの投稿'
    return render(request,'comments/form.html',context)

def comments_update(request, comment_id):
    if not request.user.is_authenticated:
        return redirect('%s?next=%s' % (settings.LOGIN_URL, request.path))
    context = {}
    context['page_title'] = 'コメントの編集'
    return render(request, 'comments/form.html', context)

def comments_delete(request,comment_id):
    if not request.user.is_authenticated:
        return redirect('%s?next=%s' % (settings.LOGIN_URL, request.path))
    return render(request, 'comments/delete_confirm.html')

def logout_view(request):
    logout(request)
    return redirect(reverse('index'))