from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse, HttpResponse
from django.views import View
from django.views.generic import ListView
from django.db.models import Q, F
from .models import Article, Category, Newsletter


class HomeView(View):
    def get(self, request):
        featured = (
            Article.objects.filter(status='published', is_featured=True)
            .select_related('category', 'author').first()
        )
        if not featured:
            featured = (Article.objects.filter(status='published')
                        .select_related('category', 'author').first())

        ex = featured.pk if featured else 0

        def region_qs(region):
            return (Article.objects
                    .filter(status='published', category__region=region)
                    .exclude(pk=ex)
                    .select_related('category', 'author')
                    .order_by('-published_at')[:6])

        trending = (Article.objects.filter(status='published')
                    .select_related('category').order_by('-views')[:8])

        return render(request, 'blog/index.html', {
            'featured': featured,
            'nigeria_articles': region_qs('nigeria'),
            'africa_articles': region_qs('africa'),
            'world_articles': region_qs('world'),
            'trending': trending,
        })


class ArticleDetailView(View):
    def get(self, request, slug):
        article = get_object_or_404(
            Article.objects.select_related('category', 'author').prefetch_related('tags'),
            slug=slug, status='published')
        Article.objects.filter(pk=article.pk).update(views=F('views') + 1)
        related = (Article.objects
                   .filter(status='published', category=article.category)
                   .exclude(pk=article.pk)
                   .select_related('category', 'author')
                   .order_by('-published_at')[:4])
        trending = (Article.objects.filter(status='published')
                    .select_related('category').order_by('-views')[:6])
        return render(request, 'blog/article_detail.html', {
            'article': article, 'related': related, 'trending': trending,
        })


class CategoryView(ListView):
    model = Article
    template_name = 'blog/category.html'
    context_object_name = 'articles'
    paginate_by = 12

    def get_queryset(self):
        self.category = get_object_or_404(Category, slug=self.kwargs['slug'])
        return (Article.objects
                .filter(status='published', category=self.category)
                .select_related('category', 'author')
                .order_by('-published_at'))

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['category'] = self.category
        ctx['trending'] = (Article.objects.filter(status='published')
                           .select_related('category').order_by('-views')[:6])
        return ctx


class SearchView(View):
    def get(self, request):
        q = request.GET.get('q', '').strip()
        articles = []
        if len(q) >= 2:
            articles = (Article.objects.filter(status='published')
                        .filter(Q(title__icontains=q) | Q(excerpt__icontains=q)
                                | Q(category__name__icontains=q))
                        .select_related('category', 'author')
                        .distinct().order_by('-published_at')[:20])
        return render(request, 'blog/search.html', {'articles': articles, 'query': q})


def newsletter_signup(request):
    if request.method == 'POST':
        email = request.POST.get('email', '').strip()
        if email:
            _, created = Newsletter.objects.get_or_create(email=email)
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return JsonResponse({'success': True, 'created': created})
    return redirect('blog:home')


def robots_txt(request):
    content = (
        "User-agent: *\nAllow: /\n"
        f"Sitemap: {request.scheme}://{request.get_host()}/sitemap.xml\n"
    )
    return HttpResponse(content, content_type='text/plain')
