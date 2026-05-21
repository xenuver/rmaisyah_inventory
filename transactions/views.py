from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, CreateView
from django.urls import reverse_lazy
from django.contrib import messages

from .models import BarangMasuk, BarangKeluar
from .forms import BarangMasukForm, BarangKeluarForm


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


class BarangMasukCreateView(LoginRequiredMixin, CreateView):
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


class BarangKeluarCreateView(LoginRequiredMixin, CreateView):
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
