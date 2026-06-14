from django.contrib.sitemaps import Sitemap
from django.urls import reverse
from .models import Article, Category


class ArticleSitemap(Sitemap):
    changefreq = 'daily'
    priority = 0.9

    def items(self):
        return Article.objects.filter(status='published').order_by('-published_at')

    def lastmod(self, obj):
        return obj.updated_at


class CategorySitemap(Sitemap):
    changefreq = 'weekly'
    priority = 0.7

    def items(self):
        return Category.objects.all()


class StaticSitemap(Sitemap):
    changefreq = 'monthly'
    priority = 0.5

    def items(self):
        return ['blog:home', 'blog:search']

    def location(self, item):
        return reverse(item)
