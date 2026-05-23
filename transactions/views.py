import csv
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, CreateView
from django.urls import reverse_lazy
from django.contrib import messages
from django.utils import timezone
from django.http import HttpResponse
from django.template.loader import get_template
from xhtml2pdf import pisa

from .models import BarangMasuk, BarangKeluar
from .forms import BarangMasukForm, BarangKeluarForm
from inventory.views import HtmxModalMixin


# ── Barang Masuk ─────────────────────────────────────────────────────────

class BarangMasukListView(LoginRequiredMixin, ListView):
    model = BarangMasuk
    template_name = 'transactions/masuk_list.html'
    context_object_name = 'masuk_list'
    paginate_by = 15

    def get_queryset(self):
        qs = super().get_queryset().select_related('barang', 'barang__satuan')
        q = self.request.GET.get('q', '').strip()
        if q:
            qs = qs.filter(barang__nama__icontains=q)
        return qs

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['page_title'] = 'Barang Masuk'
        ctx['q'] = self.request.GET.get('q', '')
        return ctx


class BarangMasukCreateView(LoginRequiredMixin, HtmxModalMixin, CreateView):
    model = BarangMasuk
    form_class = BarangMasukForm
    template_name = 'transactions/masuk_form.html'
    success_url = reverse_lazy('transactions:masuk_list')

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['page_title'] = 'Catat Barang Masuk'
        ctx['form_title'] = 'Catat Barang Masuk'
        return ctx

    def form_valid(self, form):
        messages.success(self.request, 'Barang masuk berhasil dicatat. Stok telah diperbarui.')
        return super().form_valid(form)


# ── Barang Keluar ────────────────────────────────────────────────────────

class BarangKeluarListView(LoginRequiredMixin, ListView):
    model = BarangKeluar
    template_name = 'transactions/keluar_list.html'
    context_object_name = 'keluar_list'
    paginate_by = 15

    def get_queryset(self):
        qs = super().get_queryset().select_related('barang', 'barang__satuan')
        q = self.request.GET.get('q', '').strip()
        if q:
            qs = qs.filter(barang__nama__icontains=q)
        return qs

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['page_title'] = 'Barang Keluar'
        ctx['q'] = self.request.GET.get('q', '')
        return ctx


class BarangKeluarCreateView(LoginRequiredMixin, HtmxModalMixin, CreateView):
    model = BarangKeluar
    form_class = BarangKeluarForm
    template_name = 'transactions/keluar_form.html'
    success_url = reverse_lazy('transactions:keluar_list')

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['page_title'] = 'Catat Barang Keluar'
        ctx['form_title'] = 'Catat Barang Keluar'
        return ctx

    def form_valid(self, form):
        messages.success(self.request, 'Barang keluar berhasil dicatat. Stok telah diperbarui.')
        return super().form_valid(form)


# ── Log Ledger & Ekspor ──────────────────────────────────────────────────

class LedgerListView(LoginRequiredMixin, ListView):
    template_name = 'transactions/ledger_list.html'
    context_object_name = 'ledger_list'
    paginate_by = 15

    def get_queryset(self):
        q = self.request.GET.get('q', '').strip()
        tipe = self.request.GET.get('tipe', '').strip()
        start_date = self.request.GET.get('start_date', '').strip()
        end_date = self.request.GET.get('end_date', '').strip()

        masuk_qs = BarangMasuk.objects.all().select_related('barang', 'barang__kategori', 'barang__satuan')
        keluar_qs = BarangKeluar.objects.all().select_related('barang', 'barang__kategori', 'barang__satuan')

        if q:
            masuk_qs = masuk_qs.filter(barang__nama__icontains=q)
            keluar_qs = keluar_qs.filter(barang__nama__icontains=q)
        if start_date:
            masuk_qs = masuk_qs.filter(tanggal__gte=start_date)
            keluar_qs = keluar_qs.filter(tanggal__gte=start_date)
        if end_date:
            masuk_qs = masuk_qs.filter(tanggal__lte=end_date)
            keluar_qs = keluar_qs.filter(tanggal__lte=end_date)

        items = []
        if not tipe or tipe == 'masuk':
            for m in masuk_qs:
                m.tipe = 'masuk'
                items.append(m)
        if not tipe or tipe == 'keluar':
            for k in keluar_qs:
                k.tipe = 'keluar'
                items.append(k)

        # Urutkan kronologis descending (terbaru di atas)
        items.sort(key=lambda x: x.created_at, reverse=True)
        self.unpaginated_items = items
        return items

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['q'] = self.request.GET.get('q', '')
        ctx['tipe'] = self.request.GET.get('tipe', '')
        ctx['start_date'] = self.request.GET.get('start_date', '')
        ctx['end_date'] = self.request.GET.get('end_date', '')

        # Stats berdasarkan data terfilter
        ctx['total_transaksi'] = len(self.unpaginated_items)
        ctx['total_masuk'] = sum(item.jumlah for item in self.unpaginated_items if item.tipe == 'masuk')
        ctx['total_keluar'] = sum(item.jumlah for item in self.unpaginated_items if item.tipe == 'keluar')
        ctx['page_title'] = 'Log Ledger'
        return ctx


def export_ledger_csv(request):
    q = request.GET.get('q', '').strip()
    tipe = request.GET.get('tipe', '').strip()
    start_date = request.GET.get('start_date', '').strip()
    end_date = request.GET.get('end_date', '').strip()

    masuk_qs = BarangMasuk.objects.all().select_related('barang', 'barang__kategori', 'barang__satuan')
    keluar_qs = BarangKeluar.objects.all().select_related('barang', 'barang__kategori', 'barang__satuan')

    if q:
        masuk_qs = masuk_qs.filter(barang__nama__icontains=q)
        keluar_qs = keluar_qs.filter(barang__nama__icontains=q)
    if start_date:
        masuk_qs = masuk_qs.filter(tanggal__gte=start_date)
        keluar_qs = keluar_qs.filter(tanggal__gte=start_date)
    if end_date:
        masuk_qs = masuk_qs.filter(tanggal__lte=end_date)
        keluar_qs = keluar_qs.filter(tanggal__lte=end_date)

    items = []
    if not tipe or tipe == 'masuk':
        for m in masuk_qs:
            m.tipe = 'masuk'
            items.append(m)
    if not tipe or tipe == 'keluar':
        for k in keluar_qs:
            k.tipe = 'keluar'
            items.append(k)

    items.sort(key=lambda x: x.created_at, reverse=True)

    response = HttpResponse(content_type='text/csv; charset=utf-8-sig')
    response['Content-Disposition'] = 'attachment; filename="ledger_inventaris.csv"'

    writer = csv.writer(response, delimiter=';')
    writer.writerow([
        'Tanggal & Waktu', 'Nama Barang', 'Kategori', 'Tipe', 
        'Jumlah', 'Satuan', 'Detail Info', 'Keterangan'
    ])

    for item in items:
        tgl_str = item.created_at.strftime('%Y-%m-%d %H:%M')
        jenis = 'Masuk' if item.tipe == 'masuk' else 'Keluar'
        qty = f"+{item.jumlah}" if item.tipe == 'masuk' else f"-{item.jumlah}"
        
        if item.tipe == 'masuk':
            detail = f"Supplier: {item.supplier or '—'}"
        else:
            detail = f"Alasan: {item.get_alasan_display()}"
            
        writer.writerow([
            tgl_str,
            item.barang.nama,
            item.barang.kategori.nama,
            jenis,
            qty,
            item.barang.satuan.nama,
            detail,
            item.keterangan or '—'
        ])

    return response


def export_ledger_pdf(request):
    q = request.GET.get('q', '').strip()
    tipe = request.GET.get('tipe', '').strip()
    start_date = request.GET.get('start_date', '').strip()
    end_date = request.GET.get('end_date', '').strip()

    masuk_qs = BarangMasuk.objects.all().select_related('barang', 'barang__kategori', 'barang__satuan')
    keluar_qs = BarangKeluar.objects.all().select_related('barang', 'barang__kategori', 'barang__satuan')

    if q:
        masuk_qs = masuk_qs.filter(barang__nama__icontains=q)
        keluar_qs = keluar_qs.filter(barang__nama__icontains=q)
    if start_date:
        masuk_qs = masuk_qs.filter(tanggal__gte=start_date)
        keluar_qs = keluar_qs.filter(tanggal__gte=start_date)
    if end_date:
        masuk_qs = masuk_qs.filter(tanggal__lte=end_date)
        keluar_qs = keluar_qs.filter(tanggal__lte=end_date)

    items = []
    if not tipe or tipe == 'masuk':
        for m in masuk_qs:
            m.tipe = 'masuk'
            items.append(m)
    if not tipe or tipe == 'keluar':
        for k in keluar_qs:
            k.tipe = 'keluar'
            items.append(k)

    items.sort(key=lambda x: x.created_at, reverse=True)

    template = get_template('transactions/ledger_pdf.html')
    context = {
        'ledger_list': items,
        'start_date': start_date,
        'end_date': end_date,
        'print_time': timezone.now()
    }
    html = template.render(context)

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="ledger_inventaris.pdf"'

    pisa_status = pisa.CreatePDF(html, dest=response)
    if pisa_status.err:
        return HttpResponse('Gagal membuat PDF', status=500)
    return response
