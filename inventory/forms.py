from django import forms
from .models import Barang, Kategori, Satuan


class BarangForm(forms.ModelForm):
    tanggal_kadaluarsa = forms.DateField(
        required=False,
        widget=forms.DateInput(attrs={'class': 'form-input', 'type': 'date'}),
        label='Tanggal Kadaluarsa Stok Awal',
        help_text='Masukkan tanggal kadaluarsa untuk stok awal jika ada.'
    )

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
            self.fields['stok_saat_ini'].help_text = 'Stok hanya bisa diubah melalui transaksi masuk/keluar.'
            self.fields['stok_saat_ini'].widget.attrs['class'] = 'form-input bg-slate-100 dark:bg-slate-800 cursor-not-allowed opacity-75'
            # Sembunyikan tanggal_kadaluarsa stok awal jika sedang mengedit
            self.fields['tanggal_kadaluarsa'].widget = forms.HiddenInput()
            self.fields['tanggal_kadaluarsa'].required = False

    def save(self, commit=True):
        instance = super().save(commit=False)
        if not instance.pk:
            instance._initial_tanggal_kadaluarsa = self.cleaned_data.get('tanggal_kadaluarsa')
        if commit:
            instance.save()
        return instance




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
