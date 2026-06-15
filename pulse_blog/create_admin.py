import os, django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'pulse_blog.settings')
django.setup()

from django.contrib.auth.models import User

username = os.environ.get('DJANGO_SUPERUSER_USERNAME', 'admin')
password = os.environ.get('DJANGO_SUPERUSER_PASSWORD', '')
email    = os.environ.get('DJANGO_SUPERUSER_EMAIL', '')

if not password:
    print('No password set — skipping.')
elif User.objects.filter(username=username).exists():
    print(f'User "{username}" already exists — skipping.')
else:
    User.objects.create_superuser(username, email, password)
    print(f'Superuser "{username}" created successfully.')
