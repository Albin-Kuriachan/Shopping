
from django import forms
from .models import Address

class AddressForm(forms.ModelForm):
    is_default = forms.BooleanField(label='Set as Default', required=False)

    class Meta:
        model = Address
        fields = ['first_name', 'last_name', 'phone', 'phone2', 'address_line', 'house_no', 'pin_code', 'place', 'landmark','is_default']
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control', 'autocomplete': 'off', 'placeholder': 'First Name','required':'required'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control', 'autocomplete': 'off', 'placeholder': 'Last Name','required':'required'}),
            'address_line': forms.TextInput(attrs={'class': 'form-control', 'autocomplete': 'off', 'placeholder': 'Address line','required':'required'}),
            'phone': forms.TextInput(attrs={'class': 'form-control', 'autocomplete': 'off', 'placeholder': 'Phone','minlength': '10', 'maxlength': '10','required':'required'}),
            'phone2': forms.TextInput(attrs={'class': 'form-control', 'autocomplete': 'off', 'placeholder': 'Alternate Phone', 'minlength': '10', 'maxlength': '10','required':'required'}),
            'house_no': forms.TextInput(attrs={'class': 'form-control', 'autocomplete': 'off', 'placeholder': 'House No','required':'required'}),
            'pin_code': forms.TextInput(attrs={'class': 'form-control', 'autocomplete': 'off', 'placeholder': 'Pin Code','required':'required'}),
            'place': forms.TextInput(attrs={'class': 'form-control', 'autocomplete': 'off', 'placeholder': 'Place','required':'required'}),
            'landmark': forms.TextInput(attrs={'class': 'form-control', 'autocomplete': 'off', 'placeholder': 'Landmark','required':'required'}),
        }

        def clean(self):
            cleaned_data = super().clean()
            phone = cleaned_data.get('phone')
            phone2 = cleaned_data.get('phone2')

            if phone and phone2 and phone == phone2:
                raise forms.ValidationError("Phone numbers must be different.")

            return cleaned_data



