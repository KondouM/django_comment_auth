from django.shortcuts import render

def comments_index(request):
    context = {}
    return render(request,'comments/index.html', context)

def comments_show(request, comment_id):
    context = {}
    context['comment_id'] = comment_id
    return render(request,'comments/show.html',context)

def comments_create(request):
    context = {}
    context['page_title'] = 'コメントの投稿'
    return render(request,'comments/form.html',context)

def coments_update(request, comment_id):
    context = {}
    context['page_title'] = 'コメントの編集'
    return render(request, 'comments/form.html', context)

def comments_delete(request,comment_id):
    return render(request, 'comments/delete_confirm.html')
