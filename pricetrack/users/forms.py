from django import forms
from .models import Register

DISTRICT = [
    ('thrissur', 'Thrissur'),
    ('ernakulam', 'Ernakulam'),
    ('kozhikode', 'Kozhikode'),
    ('kannur', 'Kannur')
]

class userRegister(forms.ModelForm):
    confirm_password = forms.CharField(
        max_length=20,
        label="Confirm Password",
        widget=forms.PasswordInput(attrs={'id': 'confirm', 'name': 'confirm'})
    )

    class Meta:
        model = Register
        fields = ['username', 'email', 'place', 'phone', 'district', 'image', 'password']
        widgets = {
            'username': forms.TextInput(attrs={'id': 'username', 'name': 'username'}),
            'email': forms.EmailInput(attrs={'id': 'email', 'name': 'email'}),
            'place': forms.TextInput(attrs={'id': 'place', 'name': 'place'}),
            'phone': forms.NumberInput(attrs={'id': 'phone', 'name': 'phone'}),
            'district': forms.Select(choices=DISTRICT, attrs={'id': 'district', 'name': 'district'}),
            'image': forms.FileInput(attrs={'id': 'image', 'name': 'image'}),
            'password': forms.PasswordInput(attrs={'id': 'pass', 'name': 'password'}),
        }
        labels = {
            'username': 'Username',
            'email': 'Email',
            'place': 'Place',
            'phone': 'Phone',
            'district': 'District',
            'image': 'Image',
            'password': 'Password'
        }
        help_texts = {
            'username': ' '
        }

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")

        if password != confirm_password:
            self.add_error('confirm_password', "Passwords do not match.")


class shopRegister(forms.ModelForm):
    confirm_password = forms.CharField(
        max_length=20,
        label="Confirm Password",
        widget=forms.PasswordInput(attrs={'id': 'confirm_password', 'class': 'form-control'})
    )

    class Meta:
        model = Register
        fields = ['name', 'email', 'district', 'image', 'password',
                  'shopname', 'place', 'phone', 'licensenumber']
        widgets = {
            'name': forms.TextInput(attrs={'id': 'name'}),
            'email': forms.EmailInput(attrs={'id': 'email'}),
            'district': forms.Select(choices=DISTRICT, attrs={'id': 'district'}),
            'image': forms.FileInput(attrs={'id': 'image'}),
            'password': forms.PasswordInput(attrs={'id': 'password'}),
            'shopname': forms.TextInput(attrs={'id': 'shopname'}),
            'place': forms.TextInput(attrs={'id': 'place'}),
            'phone': forms.NumberInput(attrs={'id': 'phone'}),
            'licensenumber': forms.NumberInput(attrs={'id': 'license'}),
        }

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")

        if password != confirm_password:
            self.add_error('confirm_password', "Passwords do not match.")
