from django.shortcuts import render, get_object_or_404, redirect
from django.views.decorators.http import require_POST
from django.contrib import messages
from .forms import CommentForm
from blog.models import Post


# Create your views here.


@require_POST
def comment(request, post_pk):
    # 先获取被评论的文章，因为后面需要把评论和被评论的文章关联起来。
    # 这里我们使用django提供的快捷函数 get_object_or_404,
    # 这个函数作用是获取的文章(Post)存在是，则获取，否则返回404页面给用户
    post = get_object_or_404(Post, pk=post_pk)
    # django 将用户提交的数据封装在request.POST中，这是一个类字典对象。
    form = CommentForm(request.POST)
    # 当调用form.is_valid()方法时， django自动帮我们检查表单的数据是否符合格式要求。
    if form.is_valid():
        # 检查到数据是合法的，调用表单的save方法保存数据到数据库
        # commit = False的作用是仅仅利用表单的数据生成Comment模型类的实例，但还不保存评论数据到数据库
        comment = form.save(commit=False)
        # 将评论和评论的文章关联起来
        comment.post = post
        # 最终将评论数据保存进入数据库，调用模型实例的save方法
        comment.save()
        messages.add_message(request, messages.SUCCESS,'评论发表成功!', extra_tags='sucess')
        # 重定向到post的详情页，实际当redirect函数接收一个函数的实例时，他会调用这个模型实例的get_absolute_url方法
        return redirect(post)
    # 检查到数据不合法，我们渲染一个预览页面，用于展示表单的错误
    # 注意这里被评论的文章 post 也传给模板，因为我们需要根据post来生成表单的提交地址

    context = {
        'post': post,
        'form': form,
    }
    messages.add_message(request, messages.ERROR, '评论发表失败! 请修改表单中的错误后重新提交。', extra_tags='danger')
    return render(request, 'comments/preview.html', context=context)
