from django.contrib.auth.models import User
from django.test import TestCase
from django.apps import apps
from django.urls import reverse

from blog.models import Category, Post


class PostModelTestCase(TestCase):
    def setUp(self):
        # 判断haystack的signal，测试生成的文章无需索引
        apps.get_app_config('haystack').signal_processor.teardown()
        user = User.objects.create_superuser(
            username='admin',
            email='admin@hellogithub.com',
            password='admin')
        cate = Category.objects.create(name='测试')
        self.post = Post.objects.create(
            title='测试标题',
            body='测试内容',
            category=cate,
            author=user,
        )

    def test_str_representation(self):
        self.assertEqual(self.post.__str__(), self.post.title)

    def test_auto_populate_excerpt(self):
        self.assertIsNotNone(self.post.excerpt)
        self.assertTrue(0 < len(self.post.excerpt) <= 54)

    def test_auto_populate_modified_time(self):
        self.assertIsNot(self.post.modified_time)

        old_post_modified_time = self.post.modified_time
        self.post.body = '新的测试内容'
        self.post.save()

        self.post.refresh_from_db()
        self.assertTrue(self.post.modified_time > old_post_modified_time)

    def test_get_absolute_url(self):
        expected_url = reverse('blog:detail', kwargs={'pk': self.post.pk})
        self.assertEqual(self.post.get_absolute_url(), expected_url)

    def test_increase_views(self):
        self.post.increase_click_nums()
        self.post.refresh_from_db()
        self.assertEqual(self.post.click_nums, 1)

        self.post.increase_click_nums()
        self.post.refresh_from_db()
        self.assertEqual(self.post.click_nums, 2)


