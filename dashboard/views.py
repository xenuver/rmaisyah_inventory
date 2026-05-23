import json
from datetime import timedelta

from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import F, Sum
from django.utils import timezone
from django.views.generic import TemplateView

from inventory.models import Barang, Kategori
from transactions.models import BarangMasuk, BarangKeluar


class DashboardView(LoginRequiredMixin, TemplateView):
    template_name = 'dashboard/index.html'

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        today = timezone.now().date()
        week_later = today + timedelta(days=7)

        barang_qs = Barang.objects.select_related('kategori', 'satuan')

        # Import StokBatch secara lokal untuk mencegah circular import
        from transactions.models import StokBatch

        # ── Stat Cards ───────────────────────────────────────────────
        ctx['total_barang'] = barang_qs.count()
        ctx['stok_kritis'] = barang_qs.filter(stok_saat_ini__lte=F('stok_minimal')).count()
        
        # Hitung barang unik yang memiliki batch aktif mendekati kadaluarsa
        expiring_batches_qs = StokBatch.objects.filter(
            jumlah_sekarang__gt=0,
            tanggal_kadaluarsa__isnull=False,
            tanggal_kadaluarsa__lte=week_later
        )
        ctx['mendekati_kadaluarsa'] = expiring_batches_qs.values('barang').distinct().count()
        
        ctx['transaksi_hari_ini'] = (
            BarangMasuk.objects.filter(tanggal=today).count()
            + BarangKeluar.objects.filter(tanggal=today).count()
        )

        # ── Stok Kritis List (Optimasi Database Filter) ──────────────
        ctx['kritis_items'] = list(barang_qs.filter(stok_saat_ini__lte=F('stok_minimal')))

        # ── Mendekati Kadaluarsa List ────────────────────────────────
        expiring_batches = expiring_batches_qs.select_related('barang').order_by('tanggal_kadaluarsa')[:10]
        kadaluarsa_items = []
        for batch in expiring_batches:
            kadaluarsa_items.append({
                'nama': batch.barang.nama,
                'tanggal_kadaluarsa': batch.tanggal_kadaluarsa
            })
        ctx['kadaluarsa_items'] = kadaluarsa_items

        # ── Recent Activity (last 10 combined) ───────────────────────
        recent_masuk = BarangMasuk.objects.select_related('barang', 'barang__satuan').order_by('-created_at')[:10]
        recent_keluar = BarangKeluar.objects.select_related('barang', 'barang__satuan').order_by('-created_at')[:10]

        activities = []
        for m in recent_masuk:
            activities.append({
                'type': 'masuk',
                'nama': m.barang.nama,
                'jumlah': m.jumlah,
                'satuan': m.barang.satuan.nama,
                'detail': f'dari {m.supplier}' if m.supplier else '',
                'tanggal': m.tanggal,
                'created_at': m.created_at,
            })
        for k in recent_keluar:
            activities.append({
                'type': 'keluar',
                'nama': k.barang.nama,
                'jumlah': k.jumlah,
                'satuan': k.barang.satuan.nama,
                'detail': k.get_alasan_display(),
                'tanggal': k.tanggal,
                'created_at': k.created_at,
            })
        activities.sort(key=lambda x: x['created_at'], reverse=True)
        ctx['recent_activities'] = activities[:10]

        # ── Chart: Kategori Breakdown (Doughnut) ─────────────────────
        kategori_data = (
            Barang.objects.values('kategori__nama')
            .annotate(total=Sum('stok_saat_ini'))
            .order_by('-total')
        )
        ctx['chart_kategori_labels'] = json.dumps([d['kategori__nama'] for d in kategori_data])
        ctx['chart_kategori_values'] = json.dumps([d['total'] or 0 for d in kategori_data])

        # ── Chart: Stock Trend (Last 14 days) ────────────────────────
        start_date = today - timedelta(days=13)
        dates = [(start_date + timedelta(days=i)).isoformat() for i in range(14)]

        masuk_by_date = dict(
            BarangMasuk.objects.filter(tanggal__gte=start_date)
            .values_list('tanggal')
            .annotate(total=Sum('jumlah'))
            .values_list('tanggal', 'total')
        )
        keluar_by_date = dict(
            BarangKeluar.objects.filter(tanggal__gte=start_date)
            .values_list('tanggal')
            .annotate(total=Sum('jumlah'))
            .values_list('tanggal', 'total')
        )

        masuk_values = []
        keluar_values = []
        for i in range(14):
            d = start_date + timedelta(days=i)
            masuk_values.append(masuk_by_date.get(d, 0) or 0)
            keluar_values.append(keluar_by_date.get(d, 0) or 0)

        ctx['chart_trend_labels'] = json.dumps(dates)
        ctx['chart_trend_masuk'] = json.dumps(masuk_values)
        ctx['chart_trend_keluar'] = json.dumps(keluar_values)

        ctx['page_title'] = 'Dashboard'
        return ctx

