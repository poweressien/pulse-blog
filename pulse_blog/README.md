# PULSE Blog — Django Edition

> Africa's Trending Pulse | Built with Django 4.x + PULSE dark design system

A production-ready blog covering Nigerian, African, and global trending news.

## Features
- Three content regions: NAIJA · AFRICA · WORLD with live accent-colour switching
- Featured/Breaking/Hot article flags with admin toggles
- Dynamic breaking news ticker
- 4-6 Google AdSense slots per page (auto-activates when ADSENSE_CLIENT is set)
- Auto-generated sitemap.xml and robots.txt
- RSS Feed at /feed/
- Full-text article search
- Newsletter email collection with AJAX submission
- Article view counter
- SEO meta tags, Open Graph, Twitter Cards on every page

## Quick Start

```bash
pip install -r requirements.txt
cp .env.example .env          # edit with your values
python manage.py migrate
python manage.py createsuperuser
python manage.py collectstatic --noinput
python manage.py runserver
```

Visit http://localhost:8000 for the blog.
Visit http://localhost:8000/admin/ to manage content.

## First Content Steps (Admin Panel)

1. Add Categories (Admin > Categories):
   | Name           | Region  | Icon | Color   |
   |----------------|---------|------|---------|
   | Business       | nigeria |  💼  | #00D97E |
   | Entertainment  | nigeria |  🎵  | #FF6B35 |
   | Economy        | africa  |  📈  | #F5C518 |
   | Technology     | africa  |  💻  | #22CCFF |
   | Politics       | world   |  🌐  | #FF4444 |
   | AI & Tech      | world   |  🤖  | #9B7FFF |

2. Add Breaking Ticker items (Admin > Breaking Ticker Items)

3. Add Articles — tick is_featured on your best article for the homepage hero.

## AdSense Setup

1. Sign up at https://adsense.google.com
2. Get your Publisher ID (ca-pub-XXXXXXXXXXXXXXXX)
3. In .env: ADSENSE_CLIENT=ca-pub-XXXXXXXXXXXXXXXX
4. Replace slot_id values in templates with your actual Ad Unit IDs.

Ad slot map per page:
| Slot               | Size     |
|--------------------|----------|
| Home top           | 728x90   |
| Home mid (per tab) | 728x90   |
| Sidebar rectangle  | 300x250  |
| Article top        | 728x90   |
| Article bottom     | 728x90   |
| Footer leaderboard | 728x90   |

= 4-6 impressions per page visit.

## PythonAnywhere Deployment

```bash
# In PythonAnywhere Bash console
git clone <your-repo-url> ~/pulse_blog
cd ~/pulse_blog
pip3.10 install --user -r requirements.txt

# Edit .env for production:
DEBUG=False
ALLOWED_HOSTS=yourusername.pythonanywhere.com
SECRET_KEY=<generate a 50-char random string>
ADSENSE_CLIENT=ca-pub-XXXXXXXXXXXXXXXX

python manage.py migrate
python manage.py createsuperuser
python manage.py collectstatic --noinput
```

In PythonAnywhere Web tab:
- Source code: /home/yourusername/pulse_blog
- Working dir: /home/yourusername/pulse_blog
- WSGI file: point to pulse_blog/wsgi.py
- Static files URL /static/ -> /home/yourusername/pulse_blog/staticfiles
- Static files URL /media/  -> /home/yourusername/pulse_blog/media

## Project Structure

```
pulse_blog/
├── blog/
│   ├── models.py           Article, Category, Tag, Newsletter, BreakingTicker
│   ├── views.py            Home, ArticleDetail, Category, Search, Newsletter
│   ├── admin.py            Full admin with fieldsets + colour swatch
│   ├── sitemaps.py         SEO sitemaps
│   ├── feeds.py            RSS feed
│   └── context_processors.py
├── templates/
│   ├── base.html           SEO + AdSense + fonts
│   └── blog/
│       ├── index.html      Homepage with hero + tabs
│       ├── article_detail.html
│       ├── category.html
│       ├── search.html
│       └── partials/       header, ticker, footer, card, sidebar, ad_slot
├── static/
│   ├── css/pulse.css       Full PULSE dark design system
│   └── js/pulse.js         Tabs, ticker, newsletter AJAX
└── pulse_blog/
    ├── settings.py
    └── urls.py
```

## Generating a Secret Key

```python
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```
