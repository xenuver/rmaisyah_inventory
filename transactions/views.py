from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, CreateView
from django.urls import reverse_lazy
from django.contrib import messages

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


# ── Ledger & Laporan ───────────────────────────────────────────────────────
from django.views.generic import TemplateView
from django.contrib.auth.decorators import login_required
from django.utils import timezone
import csv
from django.http import HttpResponse
from django.template.loader import get_template
from xhtml2pdf import pisa
from io import BytesIO

def get_filtered_ledger_data(request):
    q = request.GET.get('q', '').strip()
    tipe = request.GET.get('tipe', '').strip()
    tgl_mulai = request.GET.get('tanggal_mulai', '').strip()
    tgl_akhir = request.GET.get('tanggal_akhir', '').strip()

    masuk = BarangMasuk.objects.select_related('barang', 'barang__satuan').all()
    keluar = BarangKeluar.objects.select_related('barang', 'barang__satuan').all()

    if q:
        masuk = masuk.filter(barang__nama__icontains=q)
        keluar = keluar.filter(barang__nama__icontains=q)
    
    if tgl_mulai:
        masuk = masuk.filter(tanggal__gte=tgl_mulai)
        keluar = keluar.filter(tanggal__gte=tgl_mulai)
        
    if tgl_akhir:
        masuk = masuk.filter(tanggal__lte=tgl_akhir)
        keluar = keluar.filter(tanggal__lte=tgl_akhir)

    entries = []
    
    if tipe != 'keluar':
        for m in masuk:
            entries.append({
                'type': 'masuk',
                'type_display': 'Masuk',
                'barang': m.barang.nama,
                'jumlah': m.jumlah,
                'satuan': m.barang.satuan.nama,
                'supplier_atau_alasan': f"Supplier: {m.supplier}" if m.supplier else "-",
                'tanggal': m.tanggal,
                'tanggal_kadaluarsa': m.tanggal_kadaluarsa,
                'keterangan': m.keterangan,
                'created_at': m.created_at,
            })
            
    if tipe != 'masuk':
        for k in keluar:
            entries.append({
                'type': 'keluar',
                'type_display': 'Keluar',
                'barang': k.barang.nama,
                'jumlah': k.jumlah,
                'satuan': k.barang.satuan.nama,
                'supplier_atau_alasan': f"Alasan: {k.get_alasan_display()}",
                'tanggal': k.tanggal,
                'tanggal_kadaluarsa': None,
                'keterangan': k.keterangan,
                'created_at': k.created_at,
            })

    entries.sort(key=lambda x: (x['tanggal'], x['created_at']), reverse=True)
    return entries


class LedgerListView(LoginRequiredMixin, ListView):
    template_name = 'transactions/ledger_list.html'
    context_object_name = 'ledger_entries'
    paginate_by = 25

    def get_queryset(self):
        return get_filtered_ledger_data(self.request)

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['page_title'] = 'Log Ledger Inventaris'
        ctx['q'] = self.request.GET.get('q', '')
        ctx['tipe'] = self.request.GET.get('tipe', '')
        ctx['tanggal_mulai'] = self.request.GET.get('tanggal_mulai', '')
        ctx['tanggal_akhir'] = self.request.GET.get('tanggal_akhir', '')
        return ctx


@login_required
def export_ledger_pdf(request):
    entries = get_filtered_ledger_data(request)
    
    context = {
        'ledger_entries': entries,
        'page_title': 'Laporan Ledger Inventaris',
        'q': request.GET.get('q', ''),
        'tipe': request.GET.get('tipe', ''),
        'tanggal_mulai': request.GET.get('tanggal_mulai', ''),
        'tanggal_akhir': request.GET.get('tanggal_akhir', ''),
        'print_date': timezone.now(),
        'request': request,
    }
    
    template = get_template('transactions/ledger_pdf.html')
    html = template.render(context)
    
    result = BytesIO()
    pdf = pisa.pisaDocument(BytesIO(html.encode("utf-8")), result)
    
    if not pdf.err:
        response = HttpResponse(result.getvalue(), content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename="ledger_inventaris.pdf"'
        return response
        
    return HttpResponse("Terjadi kesalahan saat memproses file PDF.", status=500)


@login_required
def export_ledger_csv(request):
    entries = get_filtered_ledger_data(request)
    
    response = HttpResponse(content_type='text/csv; charset=utf-8-sig')
    response['Content-Disposition'] = 'attachment; filename="ledger_inventaris.csv"'
    
    writer = csv.writer(response, delimiter=';')
    writer.writerow(['Tanggal', 'Tipe', 'Nama Barang', 'Jumlah', 'Satuan', 'Keterangan Transaksi', 'Catatan'])
    
    for entry in entries:
        writer.writerow([
            entry['tanggal'].strftime('%Y-%m-%d'),
            entry['type_display'],
            entry['barang'],
            entry['jumlah'],
            entry['satuan'],
            entry['supplier_atau_alasan'],
            entry['keterangan']
        ])
        
    return response


