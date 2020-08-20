from django import template
from ..models import Post, Category, Tag

register = template.Library()


@register.inclusion_tag('blog/inclusions/_recent_posts.html', takes_context=True)
def show_recent_posts(context, num=5):
    """最新文章模板标签"""
    return {
        'recent_post_list': Post.objects.all().order_by('-created_time')[:num],
    }


@register.inclusion_tag('blog/inclusions/_archives.html', takes_context=True)
def show_archives(context):
    """归类模板标签"""
    return {
        'date_list': Post.objects.dates('created_time', 'month', order='DESC'),
    }


@register.inclusion_tag('blog/inclusions/_categories.html', takes_context=True)
def show_categories(context):
    """分类模板标签"""
    return {
        'category_list': Category.objects.all(),
    }


@register.inclusion_tag('blog/inclusions/_tags.html', takes_context=True)
def show_tags(context):
    """标签云模板标签"""
    return {
        'tag_list': Tag.objects.all(),
    }
