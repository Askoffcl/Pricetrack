from django import forms
from .models import Product, Feedback, Complaint, shopProduct, Available

class AddProduct(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['productname', 'productcate', 'brand', 'description', 'price', 'image']
        widgets = {
            'productname': forms.TextInput(attrs={'id': 'productname'}),
            'productcate': forms.Select( attrs={'id': 'productcate'}),
            'brand': forms.TextInput(attrs={'id': 'brand'}),
            'description': forms.Textarea(attrs={'id': 'features'}),
            'price': forms.NumberInput(attrs={'id': 'price'}),
            'image': forms.FileInput(attrs={'id': 'image'})
        }
        labels = {
            'productname': 'Product Name',
            'productcate': 'Product Category',
            'brand': 'Brand',
            'description': 'Features',
            'price': 'MRP',
            'image': 'Image'
        }

    def clean_price(self):
        price = self.cleaned_data.get('price')
        if price is None or price <= 0:
            raise forms.ValidationError("Price must be a positive number greater than zero.")
        return price



class FeedbackForm(forms.ModelForm):
    class Meta:
        model = Feedback
        fields = ['comment', 'rating']
        widgets = {
            'comment': forms.Textarea(attrs={'id': 'comments'}),
            'rating': forms.NumberInput(attrs={'id': 'rating', 'placeholder': 'Rate from 1 to 5'})
        }
        labels = {
            'comment': 'Comments',
            'rating': 'Rating'
        }

    def clean_rating(self):
        rating = self.cleaned_data.get('rating')
        if rating is None:
            raise forms.ValidationError("Rating is required.")
        if not (1 <= rating <= 5):
            raise forms.ValidationError("Rating must be between 1 and 5.")
        return rating

# ComplaintForm
class ComplaintForm(forms.ModelForm):
    class Meta:
        model = Complaint
        fields = ['description']
        widgets = {
            'description': forms.Textarea(attrs={'id': 'comments', 'placeholder': 'Any complaints'})
        }
        labels = {
            'description': ''
        }

# addShopProduct Form
class addShopProduct(forms.ModelForm):
    class Meta:
        model = shopProduct
        fields = ['model', 'color', 'price', 'image','quantityAvailable']
        widgets = {
            'model': forms.TextInput(attrs={'id': 'model'}),
            'price': forms.NumberInput(attrs={'id': 'price'}),
            'image': forms.FileInput(attrs={'id': 'image'}),
            'quantityAvailable':forms.NumberInput(attrs = {'id':'quantityAvailable'})
        }
        labels = {
            'model': 'Model',
            'color': 'Color',
            'price': 'Price',
            'image': 'Image',
            'quantityAvailable':'Quantity'
        }

    def clean_price(self):
        price = self.cleaned_data.get('price')
        if price is None or price <= 0:
            raise forms.ValidationError("Price must be a positive number greater than zero.")
        return price
    def clean_quantityAvailable(self):
        price = self.cleaned_data.get('quantityAvailable')
        if price is None or price <= 0:
            raise forms.ValidationError("Price must be a positive number greater than zero.")
        return price

# notAvailable Form
class notAvailable(forms.ModelForm):
    class Meta:
        model = Available
        fields = ['productname', 'productcate', 'brand', 'description', 'price', 'image']
        widgets = {
            'productname': forms.TextInput(attrs={'id': 'productname'}),
            'productcate': forms.Select(attrs={'id': 'productcate'}),
            'brand': forms.TextInput(attrs={'id': 'brand'}),
            'description': forms.Textarea(attrs={'id': 'features'}),
            'price': forms.NumberInput(attrs={'id': 'price'}),
            'image': forms.FileInput(attrs={'id': 'image'})
        }
        labels = {
            'productname': 'Product Name',
            'productcate': 'Product Category',
            'brand': 'Brand',
            'description': 'Features',
            'price': 'MRP',
            'image': 'Image'
        }

    def clean_price(self):
        price = self.cleaned_data.get('price')
        if price is None or price <= 0:
            raise forms.ValidationError("Price must be a positive number greater than zero.")
        return price
