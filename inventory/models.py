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
        from django.utils import timezone
        from datetime import timedelta
        week_later = timezone.now().date() + timedelta(days=7)
        return self.batches.filter(
            stok_sisa__gt=0,
            tanggal_kadaluarsa__isnull=False,
            tanggal_kadaluarsa__lte=week_later
        ).exists()

    def save(self, *args, **kwargs):
        is_new = self.pk is None
        initial_stock = 0
        if is_new:
            initial_stock = self.stok_saat_ini
            self.stok_saat_ini = 0
        
        super().save(*args, **kwargs)
        
        if is_new and initial_stock > 0:
            from transactions.models import BarangMasuk
            from django.utils import timezone
            # Dapatkan tanggal_kadaluarsa awal jika dilewatkan lewat form
            initial_exp = getattr(self, '_initial_tanggal_kadaluarsa', None)
            BarangMasuk.objects.create(
                barang=self,
                jumlah=initial_stock,
                supplier='Sistem (Stok Awal)',
                tanggal=timezone.now().date(),
                tanggal_kadaluarsa=initial_exp,
                keterangan='Stok awal saat pendaftaran barang baru.'
            )

