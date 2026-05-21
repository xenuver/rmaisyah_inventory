from django.urls import path
from . import views

app_name = 'transactions'

urlpatterns = [
    # Barang Masuk
    path('masuk/', views.BarangMasukListView.as_view(), name='masuk_list'),
    path('masuk/tambah/', views.BarangMasukCreateView.as_view(), name='masuk_create'),
    # Barang Keluar
    path('keluar/', views.BarangKeluarListView.as_view(), name='keluar_list'),
    path('keluar/tambah/', views.BarangKeluarCreateView.as_view(), name='keluar_create'),
]
