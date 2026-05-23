from django.contrib import admin
from .models import BarangMasuk, BarangKeluar, StokBatch, BarangKeluarBatch


@admin.register(BarangMasuk)
class BarangMasukAdmin(admin.ModelAdmin):
    list_display = ('barang', 'jumlah', 'supplier', 'tanggal', 'tanggal_kadaluarsa', 'created_at')
    list_filter = ('tanggal', 'tanggal_kadaluarsa')
    search_fields = ('barang__nama', 'supplier')
    date_hierarchy = 'tanggal'


@admin.register(BarangKeluar)
class BarangKeluarAdmin(admin.ModelAdmin):
    list_display = ('barang', 'jumlah', 'alasan', 'tanggal', 'created_at')
    list_filter = ('alasan', 'tanggal')
    search_fields = ('barang__nama',)
    date_hierarchy = 'tanggal'


@admin.register(StokBatch)
class StokBatchAdmin(admin.ModelAdmin):
    list_display = ('barang', 'stok_sisa', 'stok_awal', 'tanggal_kadaluarsa', 'created_at')
    list_filter = ('tanggal_kadaluarsa', 'barang')
    search_fields = ('barang__nama',)
    ordering = ('tanggal_kadaluarsa', 'created_at')


@admin.register(BarangKeluarBatch)
class BarangKeluarBatchAdmin(admin.ModelAdmin):
    list_display = ('barang_keluar', 'batch', 'jumlah')
    search_fields = ('barang_keluar__barang__nama',)

