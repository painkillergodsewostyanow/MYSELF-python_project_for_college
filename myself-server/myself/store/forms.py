from django import forms
from user.models import Certificate, User
from django.conf import settings


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
        user = User.objects.filter(email=certificate.email_recipient).last()

        if not user:
            certificate.send_notify_email(code=settings.USER_NOT_CREATED)
            return certificate

        if not user.is_email_verified:
            certificate.send_notify_email(code=settings.USER_EMAIL_NOT_VERIFIED)
            return certificate
        else:
            certificate.user = user
            certificate.save()
            certificate.send_notify_email()

        return certificate

    class Meta:
        model = Certificate
        fields = ('name_recipient', 'phone_number_recipient', 'email_recipient', 'value', 'congratulation',
                  'name_payer', 'phone_number_payer', 'email_payer')
