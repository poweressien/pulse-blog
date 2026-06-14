from django.contrib.syndication.views import Feed
from django.conf import settings
from .models import Article


class LatestArticlesFeed(Feed):
    title = getattr(settings, 'SITE_NAME', 'PULSE')
    link = '/'
    description = 'Latest trending news from Nigeria, Africa and the World'

    def items(self):
        return Article.objects.filter(status='published').order_by('-published_at')[:20]

    def item_title(self, item):
        return item.title

    def item_description(self, item):
        return item.excerpt

    def item_pubdate(self, item):
        return item.published_at

    def item_author_name(self, item):
        if item.author:
            return item.author.get_full_name() or item.author.username
        return 'PULSE Editor'
