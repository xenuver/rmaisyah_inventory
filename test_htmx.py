import os
import django
from django.test import RequestFactory
from django.contrib.auth import get_user_model

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'rmaisyah_inventory.settings')
django.setup()

from inventory.views import BarangDeleteView
from inventory.models import Barang

barang = Barang.objects.first()

factory = RequestFactory()
request = factory.get(f'/inventory/barang/{barang.pk}/hapus/', HTTP_HX_REQUEST='true')

User = get_user_model()
user = User.objects.first()
request.user = user

view = BarangDeleteView.as_view()
response = view(request, pk=barang.pk)

print("Status Code:", response.status_code)
print("Content Length:", len(response.rendered_content))
print("Content Snippet:")
print(response.rendered_content[:500])
