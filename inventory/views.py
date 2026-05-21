from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.contrib import messages

from .models import Barang, Kategori, Satuan
from .forms import BarangForm, KategoriForm, SatuanForm


# ── Barang CRUD ──────────────────────────────────────────────────────────

class BarangListView(LoginRequiredMixin, ListView):
    model = Barang
    template_name = 'inventory/barang_list.html'
    context_object_name = 'barang_list'
    paginate_by = 15

    def get_queryset(self):
        qs = super().get_queryset().select_related('kategori', 'satuan')
        q = self.request.GET.get('q', '').strip()
        kategori = self.request.GET.get('kategori', '').strip()
        if q:
            qs = qs.filter(nama__icontains=q)
        if kategori:
            qs = qs.filter(kategori_id=kategori)
        return qs

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['kategori_list'] = Kategori.objects.all()
        ctx['q'] = self.request.GET.get('q', '')
        ctx['selected_kategori'] = self.request.GET.get('kategori', '')
        ctx['page_title'] = 'Data Barang'
        return ctx


class BarangCreateView(LoginRequiredMixin, CreateView):
    model = Barang
    form_class = BarangForm
    template_name = 'inventory/barang_form.html'
    success_url = reverse_lazy('inventory:barang_list')

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['page_title'] = 'Tambah Barang'
        ctx['form_title'] = 'Tambah Barang Baru'
        return ctx

    def form_valid(self, form):
        messages.success(self.request, 'Barang berhasil ditambahkan.')
        return super().form_valid(form)


class BarangUpdateView(LoginRequiredMixin, UpdateView):
    model = Barang
    form_class = BarangForm
    template_name = 'inventory/barang_form.html'
    success_url = reverse_lazy('inventory:barang_list')

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['page_title'] = 'Edit Barang'
        ctx['form_title'] = f'Edit: {self.object.nama}'
        return ctx

    def form_valid(self, form):
        messages.success(self.request, 'Barang berhasil diperbarui.')
        return super().form_valid(form)


class BarangDeleteView(LoginRequiredMixin, DeleteView):
    model = Barang
    template_name = 'inventory/barang_confirm_delete.html'
    success_url = reverse_lazy('inventory:barang_list')

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['page_title'] = 'Hapus Barang'
        return ctx

    def form_valid(self, form):
        messages.success(self.request, f'Barang "{self.object.nama}" berhasil dihapus.')
        return super().form_valid(form)


# ── Kategori CRUD ────────────────────────────────────────────────────────

class KategoriListView(LoginRequiredMixin, ListView):
    model = Kategori
    template_name = 'inventory/kategori_list.html'
    context_object_name = 'kategori_list'

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['page_title'] = 'Kategori Barang'
        return ctx


class KategoriCreateView(LoginRequiredMixin, CreateView):
    model = Kategori
    form_class = KategoriForm
    template_name = 'inventory/kategori_form.html'
    success_url = reverse_lazy('inventory:kategori_list')

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['page_title'] = 'Tambah Kategori'
        ctx['form_title'] = 'Tambah Kategori Baru'
        return ctx

    def form_valid(self, form):
        messages.success(self.request, 'Kategori berhasil ditambahkan.')
        return super().form_valid(form)


class KategoriUpdateView(LoginRequiredMixin, UpdateView):
    model = Kategori
    form_class = KategoriForm
    template_name = 'inventory/kategori_form.html'
    success_url = reverse_lazy('inventory:kategori_list')

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['page_title'] = 'Edit Kategori'
        ctx['form_title'] = f'Edit: {self.object.nama}'
        return ctx


class KategoriDeleteView(LoginRequiredMixin, DeleteView):
    model = Kategori
    template_name = 'inventory/barang_confirm_delete.html'
    success_url = reverse_lazy('inventory:kategori_list')

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['page_title'] = 'Hapus Kategori'
        return ctx


# ── Satuan CRUD ──────────────────────────────────────────────────────────

class SatuanListView(LoginRequiredMixin, ListView):
    model = Satuan
    template_name = 'inventory/satuan_list.html'
    context_object_name = 'satuan_list'

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['page_title'] = 'Satuan Barang'
        return ctx


class SatuanCreateView(LoginRequiredMixin, CreateView):
    model = Satuan
    form_class = SatuanForm
    template_name = 'inventory/satuan_form.html'
    success_url = reverse_lazy('inventory:satuan_list')

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['page_title'] = 'Tambah Satuan'
        ctx['form_title'] = 'Tambah Satuan Baru'
        return ctx


class SatuanUpdateView(LoginRequiredMixin, UpdateView):
    model = Satuan
    form_class = SatuanForm
    template_name = 'inventory/satuan_form.html'
    success_url = reverse_lazy('inventory:satuan_list')

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['page_title'] = 'Edit Satuan'
        ctx['form_title'] = f'Edit: {self.object.nama}'
        return ctx


class SatuanDeleteView(LoginRequiredMixin, DeleteView):
    model = Satuan
    template_name = 'inventory/barang_confirm_delete.html'
    success_url = reverse_lazy('inventory:satuan_list')

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['page_title'] = 'Hapus Satuan'
        return ctx
