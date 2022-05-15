from ckeditor.fields import RichTextField
from django import forms

from accounts.models import MyUser
from .models import PropertyCategory, Property


class PropertyCategoryForm(forms.ModelForm):
    class Meta:
        model = PropertyCategory
        fields = ['category']
        widgets = {
            'category': forms.TextInput(attrs={'class': 'form-control'}),
        }


class PropertyForm(forms.ModelForm):
    class Meta:
        model = Property
        fields = [
            'user', 'photo', 'name', 'category', 'location_state',
            'location', 'status', 'price', 'desc', 'is_price_negotiable', 'is_available'
        ]
        widgets = {
            'user': forms.Select(attrs={'class': 'form-control'}),
            'name': forms.TextInput(attrs={'class': 'form-control', 'onkeydown': 'return /[a-z]/i.test(event.key)'}),
            'category': forms.Select(attrs={'class': 'form-control'}),
            'location_state': forms.Select(attrs={'class': 'form-control'}),
            'location': forms.TextInput(attrs={'class': 'form-control'}),
            'status': forms.Select(attrs={'class': 'form-control'}),
            'price': forms.NumberInput(attrs={'class': 'form-control'}),

        }

    def __init__(self, user, *args, **kwargs):
        super(PropertyForm, self).__init__(*args, **kwargs)
        self.fields['category'].empty_label = 'Select Category'
        self.fields['location_state'].empty_label = 'Select location State'
        self.fields['status'].empty_label = 'Select Status'
        self.fields['user'].empty_label = None
        self.fields['user'].queryset = MyUser.objects.filter(email=user)
