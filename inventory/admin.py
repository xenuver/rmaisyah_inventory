from django.contrib import admin
from .models import Barang, Kategori, Satuan


@admin.register(Kategori)
class KategoriAdmin(admin.ModelAdmin):
    list_display = ('nama', 'deskripsi', 'created_at')
    search_fields = ('nama',)


@admin.register(Satuan)
class SatuanAdmin(admin.ModelAdmin):
    list_display = ('nama',)
    search_fields = ('nama',)


@admin.register(Barang)
class BarangAdmin(admin.ModelAdmin):
    list_display = ('nama', 'kategori', 'satuan', 'stok_saat_ini', 'stok_minimal')
    list_filter = ('kategori', 'satuan')
    search_fields = ('nama',)

