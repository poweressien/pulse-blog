from django.contrib import admin
from django.utils.html import format_html
from .models import Article, Category, Tag, Newsletter, BreakingTicker


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'region', 'color_swatch', 'icon', 'order']
    list_editable = ['order']
    prepopulated_fields = {'slug': ('name',)}

    def color_swatch(self, obj):
        return format_html(
            '<span style="background:{};display:inline-block;width:22px;'
            'height:22px;border-radius:4px;border:1px solid #ccc"></span>',
            obj.color)
    color_swatch.short_description = 'Color'


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug']
    prepopulated_fields = {'slug': ('name',)}


@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display = ['title', 'category', 'status', 'is_featured',
                    'is_breaking', 'is_hot', 'views', 'published_at']
    list_filter = ['status', 'category__region', 'category',
                   'is_featured', 'is_breaking', 'is_hot']
    list_editable = ['status', 'is_featured', 'is_breaking', 'is_hot']
    search_fields = ['title', 'excerpt', 'content']
    prepopulated_fields = {'slug': ('title',)}
    date_hierarchy = 'published_at'
    readonly_fields = ['views', 'created_at', 'updated_at', 'read_time_display']
    filter_horizontal = ['tags']

    fieldsets = [
        ('Content', {
            'fields': ['title', 'slug', 'excerpt', 'content',
                       'featured_image', 'featured_image_alt'],
        }),
        ('Organisation', {
            'fields': ['category', 'tags', 'author'],
        }),
        ('Display Flags', {
            'fields': ['is_featured', 'is_breaking', 'is_hot'],
        }),
        ('Publishing', {
            'fields': ['status', 'published_at'],
        }),
        ('SEO', {
            'fields': ['meta_title', 'meta_description'],
            'classes': ['collapse'],
        }),
        ('Stats (read-only)', {
            'fields': ['views', 'read_time_display', 'created_at', 'updated_at'],
            'classes': ['collapse'],
        }),
    ]

    def read_time_display(self, obj):
        return obj.read_time
    read_time_display.short_description = 'Read Time'

    def save_model(self, request, obj, form, change):
        if not obj.author_id:
            obj.author = request.user
        super().save_model(request, obj, form, change)


@admin.register(Newsletter)
class NewsletterAdmin(admin.ModelAdmin):
    list_display = ['email', 'is_active', 'subscribed_at']
    list_filter = ['is_active']
    search_fields = ['email']
    readonly_fields = ['subscribed_at']


@admin.register(BreakingTicker)
class BreakingTickerAdmin(admin.ModelAdmin):
    list_display = ['text', 'is_active', 'order', 'created_at']
    list_editable = ['is_active', 'order']


admin.site.site_header = 'PULSE Admin'
admin.site.site_title = 'PULSE'
admin.site.index_title = 'Content Management'
