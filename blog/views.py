import re
import markdown

from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404
from django.views.generic import View, ListView, DetailView

from markdown.extensions.toc import TocExtension, slugify
from pure_pagination import PaginationMixin

from .models import Post, Category, Tag


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


class IndexView(PaginationMixin, ListView):
    """首页展示所有的博客文章"""
    model = Post
    template_name = 'blog/index.html'
    context_object_name = 'post_list'
    # 指定 paginate_by 属性后开启分页功能，其值代表每一页包含多少篇文章
    paginate_by = 20


class CategoryView(ListView):
    """展示类别的文章"""
    model = Post
    template_name = 'blog/index.html'
    context_object_name = 'post_list'

    def get_queryset(self):
        cate = get_object_or_404(Category, pk=self.kwargs.get('pk'))
        return super(CategoryView, self).get_queryset().filter(category=cate)


class TagView(ListView):
    """记得在开始的部分导入Category类"""
    model = Post
    template_name = 'blog/index.html'
    context_object_name = 'post_list'

    def get_queryset(self):
        t_tag = get_object_or_404(Tag, pk=self.kwargs.get('pk'))
        return super(ArchiveView, self).get_queryset().filter(tags=t_tag)


class ArchiveView(ListView):
    """归档文章列表"""
    model = Post
    template_name = 'blog/index.html'
    context_object_name = 'post_list'

    def get_queryset(self):
        m_year = self.kwargs.get('year')
        m_month = self.kwargs.get('month')
        print('year:%d,month:%d' % (m_year, m_month))
        return super(ArchiveView, self).get_queryset().filter(created_time__year=m_year,
                                                              created_time__month=m_month)


class PostDetailView(DetailView):
    """文章详情"""
    model = Post
    template_name = 'blog/detail.html'
    context_object_name = 'post'

    def get(self, request, *args, **kwargs):
        response = super(PostDetailView, self).get(request, *args, **kwargs)
        # 将文章的阅读量 +1
        self.object.increase_click_nums()

        return response

    def get_object(self, queryset=None):
        # 覆写get_object方法的目的是需要对post的body值进行渲染
        post = super().get_object(queryset=None)

        md = markdown.Markdown(extensions=[
            'markdown.extensions.extra',  # 用于标题、表格、引用这些基本转换
            'markdown.extensions.codehilite',  # 用于语法高亮
            TocExtension(slugify=slugify),  # 用于生成目录
        ])
        post.body = md.convert(post.body)
        m = re.search(r'<div class="toc">\s*<ul>(.*)</ul>\s*</div>', md.toc, re.S)
        post.toc = m.group(1) if m is not None else ''
        return post
