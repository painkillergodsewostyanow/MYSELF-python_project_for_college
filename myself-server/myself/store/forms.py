from django import forms
from user.models import Certificate, User
from store.tasks import send_notify_email


class BookCertificate(forms.ModelForm):
    name_recipient = forms.CharField(widget=forms.TextInput(attrs={
        'placeholder': 'Имя получателя'
    }))
    phone_number_recipient = forms.CharField(widget=forms.TextInput(attrs={
        'placeholder': 'Номер Телефона'
    }))
    email_recipient = forms.EmailField(widget=forms.EmailInput(attrs={
        'placeholder': 'E-mail'
    }))
    value = forms.DecimalField(widget=forms.NumberInput(attrs={
        'placeholder': 'Вы можете ввести любую сумму до 30 000 руб.',
        'onKeyUp': "document.all['final_price'].value = this.value"
    }))
    congratulation = forms.CharField(widget=forms.Textarea(attrs={
        'placeholder': 'Текст поздравления'
    }))
    name_payer = forms.CharField(widget=forms.TextInput(attrs={
        'placeholder': 'Имя'
    }))
    phone_number_payer = forms.CharField(widget=forms.TextInput(attrs={
        'placeholder': 'Номер Телефона'
    }))
    email_payer = forms.EmailField(widget=forms.EmailInput(attrs={
        'placeholder': 'E-mail'
    }))

    def save(self, commit=True):
        certificate = super(BookCertificate, self).save(commit=True)
        send_notify_email.delay(certificate.pk)

        return certificate

    class Meta:
        model = Certificate
        fields = ('name_recipient', 'phone_number_recipient', 'email_recipient', 'value', 'congratulation',
                  'name_payer', 'phone_number_payer', 'email_payer')
