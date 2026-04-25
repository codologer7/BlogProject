import os
import sys
import django
import pathlib

sys.path.insert(0, os.getcwd())
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'blogproject.settings')
django.setup()

from blogapp.models import Post

MEDIA_ROOT = pathlib.Path(os.path.join(os.getcwd(), 'media'))
def assign_default():
    default_rel = 'post_images/images.jfif'
    default_path = MEDIA_ROOT / default_rel
    if not default_path.exists():
        print('Default image not found at', default_path)
        return

    updated = 0
    for p in Post.objects.all():
        if not p.image:
            p.image = default_rel
            p.save()
            updated += 1
            print(f'Updated post id={p.id} title="{p.title}"')
    print('Done. Total updated:', updated)

if __name__ == '__main__':
    assign_default()
