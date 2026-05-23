from django.db import models, transaction
from django.core.exceptions import ValidationError
from django.utils import timezone
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
        if self.pk is not None:
            old = BarangMasuk.objects.get(pk=self.pk)
            if hasattr(old, 'batch'):
                consumed = old.jumlah - old.batch.jumlah_sekarang
                if self.jumlah < consumed:
                    raise ValidationError(
                        f"Tidak dapat mengubah jumlah barang masuk menjadi {self.jumlah}. "
                        f"Sebanyak {consumed} {self.barang.satuan.nama} dari batch ini sudah digunakan."
                    )

    @transaction.atomic
    def save(self, *args, **kwargs):
        is_new = self.pk is None
        
        # Lock barang row
        barang = Barang.objects.select_for_update().get(pk=self.barang.pk)
        
        if not is_new:
            old = BarangMasuk.objects.get(pk=self.pk)
            if old.barang == self.barang:
                self.barang.stok_saat_ini -= old.jumlah
            else:
                old_barang = Barang.objects.select_for_update().get(pk=old.barang.pk)
                old_barang.stok_saat_ini -= old.jumlah
                old_barang.save(update_fields=['stok_saat_ini'])
                
        self.barang.stok_saat_ini += self.jumlah
        self.barang.save(update_fields=['stok_saat_ini'])
        
        super().save(*args, **kwargs)
        
        # Create or update corresponding StokBatch
        if is_new:
            StokBatch.objects.create(
                barang=self.barang,
                barang_masuk=self,
                jumlah_awal=self.jumlah,
                jumlah_sekarang=self.jumlah,
                tanggal_kadaluarsa=self.tanggal_kadaluarsa
            )
        else:
            if hasattr(self, 'batch'):
                batch = self.batch
                diff = self.jumlah - old.jumlah
                batch.barang = self.barang
                batch.jumlah_awal = self.jumlah
                batch.jumlah_sekarang = batch.jumlah_sekarang + diff
                batch.tanggal_kadaluarsa = self.tanggal_kadaluarsa
                batch.save()
            else:
                StokBatch.objects.create(
                    barang=self.barang,
                    barang_masuk=self,
                    jumlah_awal=self.jumlah,
                    jumlah_sekarang=self.jumlah,
                    tanggal_kadaluarsa=self.tanggal_kadaluarsa
                )

    @transaction.atomic
    def delete(self, *args, **kwargs):
        barang = Barang.objects.select_for_update().get(pk=self.barang.pk)
        if hasattr(self, 'batch'):
            self.batch.refresh_from_db()
            if self.batch.jumlah_sekarang < self.jumlah:
                raise ValidationError(
                    f"Tidak dapat menghapus transaksi ini karena sebagian atau seluruh stok dari batch ini "
                    f"({self.jumlah - self.batch.jumlah_sekarang} {self.barang.satuan.nama}) telah dikonsumsi."
                )
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
        else:
            old = BarangKeluar.objects.get(pk=self.pk)
            available_stock = self.barang.stok_saat_ini + old.jumlah
            if available_stock < self.jumlah:
                raise ValidationError(
                    f'Stok tidak mencukupi untuk pembaruan ini. Stok tersedia (ditambah transaksi ini): {available_stock} {self.barang.satuan.nama}'
                )

    def restore_batches(self):
        junctions = self.keluar_batches.all()
        for j in junctions:
            batch = j.stok_batch
            batch.jumlah_sekarang += j.jumlah
            batch.save(update_fields=['jumlah_sekarang'])
        junctions.delete()

    @transaction.atomic
    def save(self, *args, **kwargs):
        is_new = self.pk is None
        
        # Lock barang row
        barang = Barang.objects.select_for_update().get(pk=self.barang.pk)
        
        if not is_new:
            old = BarangKeluar.objects.get(pk=self.pk)
            if old.barang == self.barang:
                old.restore_batches()
                self.barang.stok_saat_ini += old.jumlah
            else:
                old_barang = Barang.objects.select_for_update().get(pk=old.barang.pk)
                old.restore_batches()
                old_barang.stok_saat_ini += old.jumlah
                old_barang.save(update_fields=['stok_saat_ini'])
                
        # Check stock sufficiency after restoration (if any)
        if self.barang.stok_saat_ini < self.jumlah:
            raise ValidationError(
                f'Stok tidak mencukupi. Stok saat ini: {self.barang.stok_saat_ini} {self.barang.satuan.nama}'
            )
            
        self.barang.stok_saat_ini -= self.jumlah
        self.barang.save(update_fields=['stok_saat_ini'])
        
        super().save(*args, **kwargs)
        
        # FIFO deduction
        batches = StokBatch.objects.select_for_update().filter(
            barang=self.barang, 
            jumlah_sekarang__gt=0
        ).order_by(
            models.F('tanggal_kadaluarsa').asc(nulls_last=True),
            'created_at',
            'id'
        )
        
        remaining = self.jumlah
        for batch in batches:
            if remaining <= 0:
                break
            deduct_qty = min(batch.jumlah_sekarang, remaining)
            batch.jumlah_sekarang -= deduct_qty
            batch.save(update_fields=['jumlah_sekarang'])
            
            BarangKeluarBatch.objects.create(
                barang_keluar=self,
                stok_batch=batch,
                jumlah=deduct_qty
            )
            remaining -= deduct_qty
            
        if remaining > 0:
            raise ValidationError("Stok batch tidak mencukupi untuk menyelesaikan transaksi FIFO.")

    @transaction.atomic
    def delete(self, *args, **kwargs):
        barang = Barang.objects.select_for_update().get(pk=self.barang.pk)
        self.restore_batches()
        self.barang.stok_saat_ini += self.jumlah
        self.barang.save(update_fields=['stok_saat_ini'])
        super().delete(*args, **kwargs)


class StokBatch(models.Model):
    barang = models.ForeignKey(Barang, on_delete=models.CASCADE, related_name='batches')
    barang_masuk = models.OneToOneField(BarangMasuk, on_delete=models.CASCADE, related_name='batch')
    jumlah_awal = models.PositiveIntegerField()
    jumlah_sekarang = models.PositiveIntegerField()
    tanggal_kadaluarsa = models.DateField(null=True, blank=True)
    created_at = models.DateTimeField(default=timezone.now)

    class Meta:
        verbose_name = 'Stok Batch'
        verbose_name_plural = 'Stok Batch'
        ordering = ['tanggal_kadaluarsa', 'created_at']

    def __str__(self):
        exp = self.tanggal_kadaluarsa.strftime('%Y-%m-%d') if self.tanggal_kadaluarsa else 'Tanpa Exp'
        return f"{self.barang.nama} - Batch #{self.id} ({self.jumlah_sekarang}/{self.jumlah_awal}) [Exp: {exp}]"


class BarangKeluarBatch(models.Model):
    barang_keluar = models.ForeignKey(BarangKeluar, on_delete=models.CASCADE, related_name='keluar_batches')
    stok_batch = models.ForeignKey(StokBatch, on_delete=models.CASCADE, related_name='keluar_batches')
    jumlah = models.PositiveIntegerField()

    class Meta:
        verbose_name = 'Barang Keluar Batch'
        verbose_name_plural = 'Barang Keluar Batch'

    def __str__(self):
        return f"Potongan Batch #{self.stok_batch.id} untuk Keluar #{self.barang_keluar.id} ({self.jumlah})"
