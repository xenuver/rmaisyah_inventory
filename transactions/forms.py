from django import forms
from .models import BarangMasuk, BarangKeluar


class BarangMasukForm(forms.ModelForm):
    class Meta:
        model = BarangMasuk
        fields = ['barang', 'jumlah', 'supplier', 'tanggal', 'keterangan']
        widgets = {
            'barang': forms.Select(attrs={'class': 'form-select'}),
            'jumlah': forms.NumberInput(attrs={
                'class': 'form-input', 'min': '1', 'placeholder': 'Jumlah masuk'
            }),
            'supplier': forms.TextInput(attrs={
                'class': 'form-input', 'placeholder': 'Nama supplier...'
            }),
            'tanggal': forms.DateInput(attrs={
                'class': 'form-input', 'type': 'date'
            }),
            'keterangan': forms.Textarea(attrs={
                'class': 'form-input', 'rows': 3, 'placeholder': 'Keterangan tambahan (opsional)...'
            }),
        }


class BarangKeluarForm(forms.ModelForm):
    class Meta:
        model = BarangKeluar
        fields = ['barang', 'jumlah', 'alasan', 'tanggal', 'keterangan']
        widgets = {
            'barang': forms.Select(attrs={'class': 'form-select'}),
            'jumlah': forms.NumberInput(attrs={
                'class': 'form-input', 'min': '1', 'placeholder': 'Jumlah keluar'
            }),
            'alasan': forms.Select(attrs={'class': 'form-select'}),
            'tanggal': forms.DateInput(attrs={
                'class': 'form-input', 'type': 'date'
            }),
            'keterangan': forms.Textarea(attrs={
                'class': 'form-input', 'rows': 3, 'placeholder': 'Keterangan tambahan (opsional)...'
            }),
        }
