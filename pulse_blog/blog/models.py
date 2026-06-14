from django.db import models
from django.contrib.auth.models import User
from django.utils.text import slugify
from django.urls import reverse


class Category(models.Model):
    REGION_CHOICES = [
        ('nigeria', 'Nigeria'),
        ('africa', 'Africa'),
        ('world', 'World'),
    ]
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)
    description = models.TextField(blank=True)
    icon = models.CharField(max_length=10, default='📰')
    color = models.CharField(max_length=7, default='#00D97E')
    region = models.CharField(max_length=20, choices=REGION_CHOICES, default='world')
    order = models.PositiveIntegerField(default=0)

    class Meta:
        verbose_name_plural = 'Categories'
        ordering = ['order', 'name']

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('blog:category', kwargs={'slug': self.slug})

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)


class Tag(models.Model):
    name = models.CharField(max_length=50)
    slug = models.SlugField(unique=True)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)


class Article(models.Model):
    STATUS_CHOICES = [('draft', 'Draft'), ('published', 'Published')]

    title = models.CharField(max_length=300)
    slug = models.SlugField(unique=True, max_length=350)
    excerpt = models.TextField(max_length=500, help_text='Short summary for cards and SEO')
    content = models.TextField(help_text='Full article content (HTML supported)')
    category = models.ForeignKey(Category, on_delete=models.PROTECT, related_name='articles')
    tags = models.ManyToManyField(Tag, blank=True)
    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True,
                               blank=True, related_name='articles')

    featured_image = models.ImageField(upload_to='articles/%Y/%m/', blank=True, null=True)
    featured_image_alt = models.CharField(max_length=200, blank=True)

    is_featured = models.BooleanField(default=False, help_text='Show in hero section')
    is_breaking = models.BooleanField(default=False, help_text='Show breaking badge')
    is_hot = models.BooleanField(default=False, help_text='Show hot badge')

    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='draft')
    views = models.PositiveIntegerField(default=0)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    published_at = models.DateTimeField(null=True, blank=True)

    meta_title = models.CharField(max_length=200, blank=True,
                                   help_text='Leave blank to use article title')
    meta_description = models.CharField(max_length=300, blank=True,
                                         help_text='Leave blank to use excerpt')

    class Meta:
        ordering = ['-published_at', '-created_at']

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('blog:article', kwargs={'slug': self.slug})

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        if self.status == 'published' and not self.published_at:
            from django.utils import timezone
            self.published_at = timezone.now()
        super().save(*args, **kwargs)

    @property
    def read_time(self):
        word_count = len(self.content.split())
        minutes = max(1, word_count // 200)
        return f'{minutes} min read'

    @property
    def get_meta_title(self):
        return self.meta_title or self.title

    @property
    def get_meta_description(self):
        return self.meta_description or self.excerpt


class Newsletter(models.Model):
    email = models.EmailField(unique=True)
    subscribed_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.email


class BreakingTicker(models.Model):
    text = models.CharField(max_length=250)
    url = models.URLField(blank=True)
    is_active = models.BooleanField(default=True)
    order = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['order', '-created_at']
        verbose_name = 'Breaking Ticker Item'

    def __str__(self):
        return self.text[:80]
