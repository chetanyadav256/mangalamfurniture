import re

from django import forms

from .models import ContactMessage


class ContactMessageForm(forms.ModelForm):
    website = forms.CharField(required=False, widget=forms.HiddenInput())

    class Meta:
        model = ContactMessage
        fields = ("name", "phone_or_email", "message")
        widgets = {
            "name": forms.TextInput(attrs={"autocomplete": "name", "placeholder": "Your name"}),
            "phone_or_email": forms.TextInput(attrs={"autocomplete": "email", "placeholder": "Phone or email"}),
            "message": forms.Textarea(attrs={"rows": 5, "placeholder": "What can we help you find?"}),
        }

    def clean_phone_or_email(self):
        value = self.cleaned_data["phone_or_email"].strip()
        if not re.match(r"^(?:[+\d][\d ()-]{6,20}|[^@\s]+@[^@\s]+\.[^@\s]+)$", value):
            raise forms.ValidationError("Enter a valid phone number or email address.")
        return value