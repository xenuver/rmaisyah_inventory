from django import forms
from .models import Barang, Kategori, Satuan


class BarangForm(forms.ModelForm):
    class Meta:
        model = Barang
        fields = ['nama', 'kategori', 'satuan', 'stok_minimal', 'stok_saat_ini']
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
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance and self.instance.pk:
            self.fields['stok_saat_ini'].disabled = True
            self.fields['stok_saat_ini'].required = False


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
