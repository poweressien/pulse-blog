from django.urls import path
from . import views
from .feeds import LatestArticlesFeed

app_name = 'blog'

urlpatterns = [
    path('', views.HomeView.as_view(), name='home'),
    path('article/<slug:slug>/', views.ArticleDetailView.as_view(), name='article'),
    path('category/<slug:slug>/', views.CategoryView.as_view(), name='category'),
    path('search/', views.SearchView.as_view(), name='search'),
    path('newsletter/', views.newsletter_signup, name='newsletter'),
    path('feed/', LatestArticlesFeed(), name='feed'),
]
