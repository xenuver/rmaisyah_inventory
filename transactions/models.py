from django.db import models
from django.core.exceptions import ValidationError
from inventory.models import Barang


class BarangMasuk(models.Model):
    barang = models.ForeignKey(
        Barang, on_delete=models.PROTECT, related_name='masuk_set'
    )
    jumlah = models.PositiveIntegerField()
    supplier = models.CharField(max_length=200, blank=True, default='')
    tanggal = models.DateField()
    keterangan = models.TextField(blank=True, default='')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Barang Masuk'
        verbose_name_plural = 'Barang Masuk'
        ordering = ['-tanggal', '-created_at']

    def __str__(self):
        return f"Masuk: {self.barang.nama} +{self.jumlah} ({self.tanggal})"

    def save(self, *args, **kwargs):
        is_new = self.pk is None
        if not is_new:
            old = BarangMasuk.objects.get(pk=self.pk)
            self.barang.stok_saat_ini -= old.jumlah
        self.barang.stok_saat_ini += self.jumlah
        self.barang.save(update_fields=['stok_saat_ini'])
        super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        self.barang.stok_saat_ini -= self.jumlah
        self.barang.save(update_fields=['stok_saat_ini'])
        super().delete(*args, **kwargs)


class BarangKeluar(models.Model):
    class Alasan(models.TextChoices):
        PEMAKAIAN_DAPUR = 'pemakaian_dapur', 'Pemakaian Dapur'
        RUSAK = 'rusak', 'Rusak / Tidak Layak'
        KADALUARSA = 'kadaluarsa', 'Kadaluarsa'
        LAINNYA = 'lainnya', 'Lainnya'

    barang = models.ForeignKey(
        Barang, on_delete=models.PROTECT, related_name='keluar_set'
    )
    jumlah = models.PositiveIntegerField()
    alasan = models.CharField(
        max_length=20, choices=Alasan.choices, default=Alasan.PEMAKAIAN_DAPUR
    )
    tanggal = models.DateField()
    keterangan = models.TextField(blank=True, default='')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Barang Keluar'
        verbose_name_plural = 'Barang Keluar'
        ordering = ['-tanggal', '-created_at']

    def __str__(self):
        return f"Keluar: {self.barang.nama} -{self.jumlah} ({self.tanggal})"

    def clean(self):
        if self.pk is None:
            if self.barang.stok_saat_ini < self.jumlah:
                raise ValidationError(
                    f'Stok tidak mencukupi. Stok saat ini: {self.barang.stok_saat_ini} {self.barang.satuan.nama}'
                )

    def save(self, *args, **kwargs):
        is_new = self.pk is None
        if not is_new:
            old = BarangKeluar.objects.get(pk=self.pk)
            self.barang.stok_saat_ini += old.jumlah
        self.barang.stok_saat_ini -= self.jumlah
        self.barang.save(update_fields=['stok_saat_ini'])
        super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        self.barang.stok_saat_ini += self.jumlah
        self.barang.save(update_fields=['stok_saat_ini'])
        super().delete(*args, **kwargs)
