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
    # Log Ledger
    path('ledger/', views.LedgerListView.as_view(), name='ledger_list'),
    path('ledger/export/csv/', views.export_ledger_csv, name='ledger_csv'),
    path('ledger/export/pdf/', views.export_ledger_pdf, name='ledger_pdf'),
]
