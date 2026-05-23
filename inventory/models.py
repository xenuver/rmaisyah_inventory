from django.db import models


class Kategori(models.Model):
    nama = models.CharField(max_length=100, unique=True)
    deskripsi = models.TextField(blank=True, default='')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Kategori'
        verbose_name_plural = 'Kategori'
        ordering = ['nama']

    def __str__(self):
        return self.nama


class Satuan(models.Model):
    nama = models.CharField(max_length=50, unique=True)

    class Meta:
        verbose_name = 'Satuan'
        verbose_name_plural = 'Satuan'
        ordering = ['nama']

    def __str__(self):
        return self.nama


class Barang(models.Model):
    nama = models.CharField(max_length=200)
    kategori = models.ForeignKey(
        Kategori, on_delete=models.PROTECT, related_name='barang_set'
    )
    satuan = models.ForeignKey(
        Satuan, on_delete=models.PROTECT, related_name='barang_set'
    )
    stok_minimal = models.PositiveIntegerField(
        default=0, help_text='Batas minimum stok sebelum sistem merekomendasikan pemesanan ulang'
    )
    stok_saat_ini = models.IntegerField(default=0)
    tanggal_kadaluarsa = models.DateField(
        null=True, blank=True, help_text='Kosongkan jika tidak memiliki tanggal kadaluarsa'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Barang'
        verbose_name_plural = 'Barang'
        ordering = ['nama']

    def __str__(self):
        return f"{self.nama} ({self.stok_saat_ini} {self.satuan.nama})"

    @property
    def is_stok_kritis(self):
        return self.stok_saat_ini <= self.stok_minimal

    @property
    def is_mendekati_kadaluarsa(self):
        if not self.tanggal_kadaluarsa:
            return False
        from django.utils import timezone
        from datetime import timedelta
        return self.tanggal_kadaluarsa <= (timezone.now().date() + timedelta(days=7))
