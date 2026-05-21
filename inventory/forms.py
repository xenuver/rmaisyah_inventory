from django import forms
from .models import Barang, Kategori, Satuan


class BarangForm(forms.ModelForm):
    class Meta:
        model = Barang
        fields = ['nama', 'kategori', 'satuan', 'stok_minimal', 'stok_saat_ini', 'tanggal_kadaluarsa']
        widgets = {
            'nama': forms.TextInput(attrs={
                'class': 'form-input', 'placeholder': 'Nama bahan baku...'
            }),
            'kategori': forms.Select(attrs={'class': 'form-select'}),
            'satuan': forms.Select(attrs={'class': 'form-select'}),
            'stok_minimal': forms.NumberInput(attrs={
                'class': 'form-input', 'min': '0'
            }),
            'stok_saat_ini': forms.NumberInput(attrs={
                'class': 'form-input', 'min': '0'
            }),
            'tanggal_kadaluarsa': forms.DateInput(attrs={
                'class': 'form-input', 'type': 'date'
            }),
        }


class KategoriForm(forms.ModelForm):
    class Meta:
        model = Kategori
        fields = ['nama', 'deskripsi']
        widgets = {
            'nama': forms.TextInput(attrs={
                'class': 'form-input', 'placeholder': 'Nama kategori...'
            }),
            'deskripsi': forms.Textarea(attrs={
                'class': 'form-input', 'rows': 3, 'placeholder': 'Deskripsi kategori (opsional)...'
            }),
        }


class SatuanForm(forms.ModelForm):
    class Meta:
        model = Satuan
        fields = ['nama']
        widgets = {
            'nama': forms.TextInput(attrs={
                'class': 'form-input', 'placeholder': 'Nama satuan (Kg, Liter, Ikat...)'
            }),
        }
