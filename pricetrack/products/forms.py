from django import forms
from . models import Product,Feedback,Complaint

BRAND = [
    ('APPLE','APPLE'),
    ('SAMSUNG','SAMSUNG'),
    ('SONY','SONY'),
    
]

class AddProduct(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['productname','productcate','brand','model','description','price','image']

        widgets = {
            'productname':forms.TextInput(attrs = {'id':'productname'}),
            'productcate':forms.TextInput(attrs = {'id':'productcate'}),
            'brand':forms.Select(choices=BRAND,attrs = {'id':'brand'}),
            'model':forms.TextInput(attrs = {'id':'model'}),
            'description':forms.Textarea(attrs={'id':'features'}),
            'price':forms.NumberInput(attrs={'id':'price'}),
            'image':forms.FileInput(attrs={'id': 'image'})
        }
        labels = {
                'productname':'Product Name','productcate':'Product Category','brand':'Brand','model':'Model','description':'Features','price':'MRP','image':'image'
            }


class FeedbackForm(forms.ModelForm):
    class Meta:
        model = Feedback
        fields = ['comment','rating']

        widgets = {
            'comment': forms.Textarea(attrs = {'id':'comments'}),
            'rating': forms.NumberInput( attrs = {'id':'rating', 'placeholder': 'Rate from 1 to 5'})
        }
        labels = {
            'comment':'Comments','rating':'Rating'
        }

    
class ComplaintForm(forms.ModelForm):
    class Meta:
        model = Complaint
        fields = ['description']

        widgets = {'description': forms.Textarea(attrs = {'id':'comments','placeholder':'Any complaints'})
        }

        labels = {
            'description':'Complaint'
        }
