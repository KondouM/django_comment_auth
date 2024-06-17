from django.conf import settings
from django.shortcuts import render
from django.shortcuts import get_object_or_404
from django.contrib.auth import authenticate,login,logout
from django.shortcuts import redirect
from django.urls import reverse

from .models import Comment
from .forms import CommentForm
from .forms import UserForm
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib import messages

def paginate_queryset(request, queryset, count):
    paginator = Paginator(queryset, count)
    page = request.GET.get('page')
    try:
        page_obj = paginator.page(page)
    except PageNotAnInteger:
        page_obj = paginator.page(1)
    except EmptyPage:
        page_obj = paginator.page(paginator.num_pages)
    return page_obj

def comments_index(request):
    if not request.user.is_authenticated:
        return redirect('%s?next=%s' % (settings.LOGIN_URL, request.path))
    # context = {}
    # context['comments'] = Comment.objects.all()
    paginate = request.GET.get(key="paginate", default="2")
    comments_list = Comment.objects.all()
    page_obj = paginate_queryset(request, comments_list, paginate)
    context = {
        'comments' : page_obj.object_list,
        'page_obj': page_obj,
        'paginate': paginate,
    }
    return render(request,'comments/index.html', context)

def comments_show(request, comment_id):
    if not request.user.is_authenticated:
        return redirect('%s?next=%s' % (settings.LOGIN_URL, request.path))
    context = {}
    # context['comment_id'] = comment_id
    comment = get_object_or_404(Comment, pk=comment_id)
    context['comment'] = comment
    context['is_owner'] = comment.is_owner(request.user)
    return render(request,'comments/show.html',context)

def comments_create(request):
    if not request.user.is_authenticated:
        return redirect('%s?next=%s' % (settings.LOGIN_URL, request.path))
    # context = {}
    # context['page_title'] = 'コメントの投稿'
    # return render(request, 'comments/form.html', context)
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = Comment()
            comment.title = form.cleaned_data.get("title")
            comment.body = form.cleaned_data.get("body")
            comment.owner_id = request.user.id
            comment.save()
            messages.success(request, '投稿しました')
            return redirect(reverse('comments:index'))
        else:
            # エラーメッセージをつけて返す
            context = {}
            context['page_title'] = 'コメントの投稿'
            context['form_name'] = 'コメントの投稿'
            context['button_label'] = 'コメントを投稿する'
            context['form'] = form
            return render(request, 'comments/form.html', context)
    else:
        context = {}
        context['form'] = CommentForm(
                            initial={
                                # 'title' : 'title',
                            }
                        )
        context['page_title'] = 'コメントの投稿'
        context['form_name'] = 'コメントの投稿'
        context['button_label'] = 'コメントを投稿する'
        return render(request, 'comments/form.html', context)

def comments_update(request, comment_id):
    if not request.user.is_authenticated:
        return redirect('%s?next=%s' % (settings.LOGIN_URL, request.path))
    context = {}
    context['page_title'] = 'コメントの編集'
    return render(request, 'comments/form.html', context)

def comments_delete(request, comment_id):
    if not request.user.is_authenticated:
        return redirect('%s?next=%s' % (settings.LOGIN_URL, request.path))
    # return render(request, 'comments/delete_confirm.html')
    if request.method == 'POST':
        comment = get_object_or_404(Comment, pk=comment_id)
        if comment.is_owner(request.user) == False:
            messages.success(request, '他ユーザのコメントは削除できません')
            return redirect(reverse('comments:index'))
        comment.delete()
        messages.success(request, 'コメントを削除しました')
        return redirect(reverse('comments:index'))
    else:
        context = {}
        comment = get_object_or_404(Comment, pk=comment_id)
        if comment.is_owner(request.user) == False:
            messages.success(request, '他ユーザのコメントは削除できません')
            return redirect(reverse('comments:index'))
        context['id'] = comment_id
        context['title'] = comment.title
        context['body'] = comment.body
        context['page_title'] = 'コメントの削除'
        context['form_name'] = 'コメントを削除しますか'
        context['button_label'] = 'コメントを削除する'
        return render(request, 'comments/delete_confirm.html', context)

def profile(request):
    if not request.user.is_authenticated:
        return redirect('%s?next=%s' % (settings.LOGIN_URL, request.path))
    context = {}
    context['user'] = request.user
    return render(request, 'profile/show.html', context)

def profile_update(request, user_id):
    if not request.user.is_authenticated:
        return redirect('%s?next=%s' % (settings.LOGIN_URL, request.path))
    if user_id != request.user.id:
            messages.success(request, '他ユーザのProfileは編集できません')
            return redirect(reverse('comments:index'))
    if request.method == 'POST':
        form = UserForm(request.POST)
        if form.is_valid():
            user = request.user
            user.first_name = form.cleaned_data.get('first_name')
            user.last_name = form.cleaned_data.get('last_name')
            user.save()
            messages.success(request, '更新しました')
            return redirect(reverse('comments:profile'))
        else:
            # エラーメッセージをつけて返す
            context = {}
            context['form'] = form
            return render(request, 'profile/profile_form.html', context)
    else:
        context = {}
        context['user'] = request.user
        context['user_id'] = user_id
        context['form'] = UserForm(
                                initial={
                                    'first_name' : request.user.first_name,
                                    'last_name' : request.user.last_name,
                                }
                            )
        return render(request, 'profile/profile_form.html', context)

def logout_view(request):
    logout(request)
    return redirect(reverse('index'))