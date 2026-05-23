from django.contrib import admin
from .models import BarangMasuk, BarangKeluar


@admin.register(BarangMasuk)
class BarangMasukAdmin(admin.ModelAdmin):
    list_display = ('barang', 'jumlah', 'supplier', 'tanggal', 'created_at')
    list_filter = ('tanggal',)
    search_fields = ('barang__nama', 'supplier')
    date_hierarchy = 'tanggal'


@admin.register(BarangKeluar)
class BarangKeluarAdmin(admin.ModelAdmin):
    list_display = ('barang', 'jumlah', 'alasan', 'tanggal', 'created_at')
    list_filter = ('alasan', 'tanggal')
    search_fields = ('barang__nama',)
    date_hierarchy = 'tanggal'
