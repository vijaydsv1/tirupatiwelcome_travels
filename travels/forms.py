from django import forms
from .models import GalleryImage, Booking

class GalleryImageForm(forms.ModelForm):
    class Meta:
        model = GalleryImage
        fields = ['title', 'image']


class BookingForm(forms.ModelForm):
    class Meta:
        model = Booking
        fields = ["full_name", "email", "phone", "service", "pickup", "drop", "message"]
        widgets = {
            "service": forms.Select(attrs={"class": "input"}),
            "message": forms.Textarea(attrs={"rows": 4}),
        }

    def clean_phone(self):
        p = self.cleaned_data["phone"]
        return p.strip()

