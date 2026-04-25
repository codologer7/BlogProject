import os
import sys
import django
import pathlib

# Ensure project root is on sys.path so Django settings module can be imported
sys.path.insert(0, os.getcwd())
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'blogproject.settings')
django.setup()

from blogapp.models import Post

MEDIA_ROOT = pathlib.Path(os.path.join(os.getcwd(), 'media'))
print('MEDIA_ROOT:', MEDIA_ROOT.resolve())

posts = Post.objects.all()
print('Total posts:', posts.count())

for p in posts:
    img_field = str(p.image) if p.image else ''
    img_exists = False
    if img_field:
        img_path = MEDIA_ROOT / img_field
        img_exists = img_path.exists()
    print(f'ID={p.id} | title="{p.title}" | image_field="{img_field}" | file_exists={img_exists} | url=/media/{img_field}')
