from django import forms
from .models import Certificate


class BookCertificate(forms.ModelForm):
    class Meta:
        model = Certificate
        fields = ('name_recipient', 'phone_number_recipient', 'email_recipient', 'value', 'congratulation',
                  'name_payer', 'phone_number_payer', 'email_payer')
