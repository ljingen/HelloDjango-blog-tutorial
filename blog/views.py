import re

from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404

import markdown

from .models import Post, Category,Tag


# Create your views here.


def index(request):
    post_list = Post.objects.all().order_by('-created_time')

    return render(request, 'blog/index.html', context={'post_list': post_list})


def detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    # 点击阅读量 +1
    post.increase_click_nums()

    md = markdown.Markdown(extensions=[
        'markdown.extensions.extra',  # 用于标题、表格、引用这些基本转换
        'markdown.extensions.codehilite',  # 用于语法高亮
        'markdown.extensions.toc',  # 用于生成目录
    ])
    post.body = md.convert(post.body)
    m = re.search(r'<div class="toc">\s*<ul>(.*)</ul>\s*</div>', md.toc, re.S)
    post.toc = m.group(1) if m is not None else ''

    # post.body = markdown.markdown(post.body,
    #                               extensions=[
    #                                   'markdown.extensions.extra',
    #                                   'markdown.extensions.codehilite',
    #                                   'markdown.extensions.toc',
    #                               ])

    return render(request, 'blog/detail.html', context={'post': post})


def archive(request, year, month):
    """根据年份月份查询文章"""
    print("the length of (%d) is %d" % (year, month))

    post_list = Post.objects.filter(created_time__year=year,
                                    created_time__month=month
                                    ).order_by('-created_time')
    return render(request, 'blog/index.html', context={'post_list': post_list})


def category(request, pk):
    """记得在开始的部分导入Category类"""
    cate = get_object_or_404(Category, pk=pk)
    post_list = Post.objects.filter(category=cate).order_by('-created_time')
    return render(request, 'blog/index.html', context={'post_list': post_list})


def tag(request, pk):
    """记得在开始的部分导入Category类"""
    t = get_object_or_404(Tag, pk=pk)
    post_list = Post.objects.filter(tags=t).order_by('-created_time')
    return render(request, 'blog/index.html', context={'post_list': post_list})

