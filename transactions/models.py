from django.db import models, transaction
from django.core.exceptions import ValidationError
from inventory.models import Barang


class BarangMasuk(models.Model):
    barang = models.ForeignKey(
        Barang, on_delete=models.PROTECT, related_name='masuk_set'
    )
    jumlah = models.PositiveIntegerField()
    supplier = models.CharField(max_length=200, blank=True, default='')
    tanggal = models.DateField()
    tanggal_kadaluarsa = models.DateField(
        null=True, blank=True, help_text='Kosongkan jika tidak memiliki tanggal kadaluarsa'
    )
    keterangan = models.TextField(blank=True, default='')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Barang Masuk'
        verbose_name_plural = 'Barang Masuk'
        ordering = ['-tanggal', '-created_at']

    def __str__(self):
        return f"Masuk: {self.barang.nama} +{self.jumlah} ({self.tanggal})"

    def clean(self):
        super().clean()
        if self.pk is not None:
            old = BarangMasuk.objects.get(pk=self.pk)
            # Jika mengubah barang
            if old.barang != self.barang:
                if hasattr(old, 'batch') and old.batch.stok_sisa < old.batch.stok_awal:
                    raise ValidationError(
                        f"Tidak dapat mengubah barang karena stok dari transaksi masuk ini sudah mulai dikonsumsi."
                    )
            # Jika mengurangi jumlah masuk
            elif self.jumlah < old.jumlah:
                if hasattr(old, 'batch'):
                    consumed = old.batch.stok_awal - old.batch.stok_sisa
                    if self.jumlah < consumed:
                        raise ValidationError(
                            f"Tidak dapat mengurangi jumlah masuk menjadi {self.jumlah} karena {consumed} item dari batch ini sudah dikonsumsi."
                        )

    def save(self, *args, **kwargs):
        with transaction.atomic():
            is_new = self.pk is None
            if not is_new:
                # Kunci data lama di database
                old = BarangMasuk.objects.select_for_update().get(pk=self.pk)
                if old.barang == self.barang:
                    diff = self.jumlah - old.jumlah
                    # Update batch sisa
                    if hasattr(old, 'batch'):
                        old.batch.stok_awal = self.jumlah
                        old.batch.stok_sisa += diff
                        old.batch.tanggal_kadaluarsa = self.tanggal_kadaluarsa
                        old.batch.save()
                    
                    # Update cached stock
                    old.barang.stok_saat_ini += diff
                    old.barang.save(update_fields=['stok_saat_ini'])
                else:
                    # Kembalikan stok barang lama
                    if hasattr(old, 'batch'):
                        old.barang.stok_saat_ini -= old.batch.stok_sisa
                        old.barang.save(update_fields=['stok_saat_ini'])
                    
                    # Hubungkan ke barang baru
                    self.barang.refresh_from_db()
            
            # Simpan data transaksi masuk
            super().save(*args, **kwargs)
            
            # Buat/Update batch barang
            if is_new:
                StokBatch.objects.create(
                    barang=self.barang,
                    barang_masuk=self,
                    stok_awal=self.jumlah,
                    stok_sisa=self.jumlah,
                    tanggal_kadaluarsa=self.tanggal_kadaluarsa
                )
                self.barang.stok_saat_ini += self.jumlah
                self.barang.save(update_fields=['stok_saat_ini'])
            else:
                if old.barang != self.barang:
                    # Hapus batch lama, buat batch baru
                    if hasattr(old, 'batch'):
                        old.batch.delete()
                    StokBatch.objects.create(
                        barang=self.barang,
                        barang_masuk=self,
                        stok_awal=self.jumlah,
                        stok_sisa=self.jumlah,
                        tanggal_kadaluarsa=self.tanggal_kadaluarsa
                    )
                    self.barang.stok_saat_ini += self.jumlah
                    self.barang.save(update_fields=['stok_saat_ini'])

    def delete(self, *args, **kwargs):
        with transaction.atomic():
            if hasattr(self, 'batch'):
                self.batch.refresh_from_db()
                if self.batch.stok_sisa < self.batch.stok_awal:
                    raise ValidationError(
                        "Tidak dapat menghapus transaksi ini karena sebagian atau seluruh stok dari batch ini sudah digunakan."
                    )
            
            barang = Barang.objects.select_for_update().get(pk=self.barang.pk)
            barang.stok_saat_ini -= self.jumlah
            barang.save(update_fields=['stok_saat_ini'])
            super().delete(*args, **kwargs)


class StokBatch(models.Model):
    barang = models.ForeignKey(
        Barang, on_delete=models.CASCADE, related_name='batches'
    )
    barang_masuk = models.OneToOneField(
        BarangMasuk, on_delete=models.CASCADE, related_name='batch'
    )
    stok_awal = models.PositiveIntegerField()
    stok_sisa = models.PositiveIntegerField()
    tanggal_kadaluarsa = models.DateField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Stok Batch'
        verbose_name_plural = 'Stok Batch'
        ordering = ['tanggal_kadaluarsa', 'created_at']

    def __str__(self):
        expiry = f" (Exp: {self.tanggal_kadaluarsa})" if self.tanggal_kadaluarsa else " (No Exp)"
        return f"Batch {self.barang.nama} - Sisa: {self.stok_sisa}/{self.stok_awal}{expiry}"


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
        super().clean()
        if self.pk is None:
            available_stock = self.barang.stok_saat_ini
        else:
            old = BarangKeluar.objects.get(pk=self.pk)
            if old.barang == self.barang:
                available_stock = self.barang.stok_saat_ini + old.jumlah
            else:
                available_stock = self.barang.stok_saat_ini
        
        if available_stock < self.jumlah:
            raise ValidationError(
                f'Stok tidak mencukupi. Stok yang tersedia: {available_stock} {self.barang.satuan.nama}'
            )

    def save(self, *args, **kwargs):
        with transaction.atomic():
            is_new = self.pk is None
            
            # Jika update, kembalikan dulu stok batch yang dipotong transaksi lama
            if not is_new:
                old = BarangKeluar.objects.select_for_update().get(pk=self.pk)
                for ded in old.batch_deductions.all():
                    batch = StokBatch.objects.select_for_update().get(pk=ded.batch.pk)
                    batch.stok_sisa += ded.jumlah
                    batch.save(update_fields=['stok_sisa'])
                
                old.barang.stok_saat_ini += old.jumlah
                old.barang.save(update_fields=['stok_saat_ini'])
                
                # Hapus catatan pemotongan lama
                old.batch_deductions.all().delete()
                self.barang.refresh_from_db()
            
            # Simpan transaksi barang keluar
            super().save(*args, **kwargs)
            
            # Potong stok batch secara FIFO (First In First Out)
            # Urutkan berdasarkan tanggal kadaluarsa terkecil (null ditempatkan paling belakang), lalu tanggal pembuatan batch
            remaining_to_deduct = self.jumlah
            batches = StokBatch.objects.filter(
                barang=self.barang,
                stok_sisa__gt=0
            ).order_by(
                models.F('tanggal_kadaluarsa').asc(nulls_last=True),
                'created_at'
            )
            
            for batch in batches:
                if remaining_to_deduct <= 0:
                    break
                
                deduct_qty = min(batch.stok_sisa, remaining_to_deduct)
                batch.stok_sisa -= deduct_qty
                batch.save(update_fields=['stok_sisa'])
                
                BarangKeluarBatch.objects.create(
                    barang_keluar=self,
                    batch=batch,
                    jumlah=deduct_qty
                )
                
                remaining_to_deduct -= deduct_qty
            
            if remaining_to_deduct > 0:
                raise ValidationError("Stok fisik dari batch yang tersedia tidak mencukupi (FIFO).")
            
            # Kurangi cached stock
            self.barang.stok_saat_ini -= self.jumlah
            self.barang.save(update_fields=['stok_saat_ini'])

    def delete(self, *args, **kwargs):
        with transaction.atomic():
            # Kembalikan stok ke batch-batch semula
            for ded in self.batch_deductions.all():
                batch = StokBatch.objects.select_for_update().get(pk=ded.batch.pk)
                batch.stok_sisa += ded.jumlah
                batch.save(update_fields=['stok_sisa'])
            
            barang = Barang.objects.select_for_update().get(pk=self.barang.pk)
            barang.stok_saat_ini += self.jumlah
            barang.save(update_fields=['stok_saat_ini'])
            
            super().delete(*args, **kwargs)


class BarangKeluarBatch(models.Model):
    barang_keluar = models.ForeignKey(
        BarangKeluar, on_delete=models.CASCADE, related_name='batch_deductions'
    )
    batch = models.ForeignKey(
        StokBatch, on_delete=models.CASCADE, related_name='deductions'
    )
    jumlah = models.PositiveIntegerField()

    class Meta:
        verbose_name = 'Pemotongan Batch Barang Keluar'
        verbose_name_plural = 'Pemotongan Batch Barang Keluar'

