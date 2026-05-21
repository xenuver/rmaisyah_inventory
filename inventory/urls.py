from django.urls import path
from . import views

app_name = 'inventory'

urlpatterns = [
    # Barang
    path('', views.BarangListView.as_view(), name='barang_list'),
    path('tambah/', views.BarangCreateView.as_view(), name='barang_create'),
    path('<int:pk>/edit/', views.BarangUpdateView.as_view(), name='barang_update'),
    path('<int:pk>/hapus/', views.BarangDeleteView.as_view(), name='barang_delete'),
    # Kategori
    path('kategori/', views.KategoriListView.as_view(), name='kategori_list'),
    path('kategori/tambah/', views.KategoriCreateView.as_view(), name='kategori_create'),
    path('kategori/<int:pk>/edit/', views.KategoriUpdateView.as_view(), name='kategori_update'),
    path('kategori/<int:pk>/hapus/', views.KategoriDeleteView.as_view(), name='kategori_delete'),
    # Satuan
    path('satuan/', views.SatuanListView.as_view(), name='satuan_list'),
    path('satuan/tambah/', views.SatuanCreateView.as_view(), name='satuan_create'),
    path('satuan/<int:pk>/edit/', views.SatuanUpdateView.as_view(), name='satuan_update'),
    path('satuan/<int:pk>/hapus/', views.SatuanDeleteView.as_view(), name='satuan_delete'),
]
