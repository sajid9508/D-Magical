from django import forms
from django.utils import timezone
from salon.models import Appointment, Inquiry, Service
import datetime

class AppointmentForm(forms.ModelForm):
    class Meta:
        model = Appointment
        fields = [
            'customer_name', 
            'customer_email', 
            'customer_phone', 
            'service', 
            'date', 
            'time', 
            'payment_method'
        ]
        widgets = {
            'customer_name': forms.TextInput(attrs={
                'class': 'w-full px-4 py-3 rounded-lg bg-slate-900 border border-slate-700 text-white focus:outline-none focus:border-brand-gold',
                'placeholder': 'Your Full Name'
            }),
            'customer_email': forms.EmailInput(attrs={
                'class': 'w-full px-4 py-3 rounded-lg bg-slate-900 border border-slate-700 text-white focus:outline-none focus:border-brand-gold',
                'placeholder': 'Your Email Address'
            }),
            'customer_phone': forms.TextInput(attrs={
                'class': 'w-full px-4 py-3 rounded-lg bg-slate-900 border border-slate-700 text-white focus:outline-none focus:border-brand-gold',
                'placeholder': '10-digit Phone Number (e.g. 9740637692)'
            }),
            'service': forms.Select(attrs={
                'class': 'w-full px-4 py-3 rounded-lg bg-slate-900 border border-slate-700 text-white focus:outline-none focus:border-brand-gold'
            }),
            'date': forms.DateInput(attrs={
                'type': 'date',
                'class': 'w-full px-4 py-3 rounded-lg bg-slate-900 border border-slate-700 text-white focus:outline-none focus:border-brand-gold'
            }),
            'time': forms.TimeInput(attrs={
                'type': 'time',
                'class': 'w-full px-4 py-3 rounded-lg bg-slate-900 border border-slate-700 text-white focus:outline-none focus:border-brand-gold'
            }),
            'payment_method': forms.RadioSelect(attrs={
                'class': 'hidden'
            })
        }

    def __init__(self, *args, **kwargs):
        super(AppointmentForm, self).__init__(*args, **kwargs)
        # Sort service field choices alphabetically
        self.fields['service'].queryset = Service.objects.all().order_by('category', 'name')
        # Remove default empty choice for payment_method and set standard choices
        self.fields['payment_method'].empty_label = None

    def clean_date(self):
        date = self.cleaned_data.get('date')
        if date:
            today = timezone.localdate()
            if date < today:
                raise forms.ValidationError("You cannot book an appointment in the past.")
            if date > today + datetime.timedelta(days=30):
                raise forms.ValidationError("Appointments can only be booked up to 30 days in advance.")
        return date

    def clean_customer_phone(self):
        phone = self.cleaned_data.get('customer_phone')
        if phone:
            # Strip spaces, dashes, etc.
            cleaned_phone = ''.join(char for char in phone if char.isdigit())
            if len(cleaned_phone) < 10 or len(cleaned_phone) > 12:
                raise forms.ValidationError("Please enter a valid 10-digit phone number.")
            return cleaned_phone
        return phone


class InquiryForm(forms.ModelForm):
    class Meta:
        model = Inquiry
        fields = ['name', 'email', 'phone', 'message']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'w-full px-4 py-3 rounded-lg bg-slate-900 border border-slate-700 text-white focus:outline-none focus:border-brand-gold',
                'placeholder': 'Your Full Name'
            }),
            'email': forms.EmailInput(attrs={
                'class': 'w-full px-4 py-3 rounded-lg bg-slate-900 border border-slate-700 text-white focus:outline-none focus:border-brand-gold',
                'placeholder': 'Your Email Address'
            }),
            'phone': forms.TextInput(attrs={
                'class': 'w-full px-4 py-3 rounded-lg bg-slate-900 border border-slate-700 text-white focus:outline-none focus:border-brand-gold',
                'placeholder': 'Your Phone Number (e.g. 9740637692)'
            }),
            'message': forms.Textarea(attrs={
                'rows': 4,
                'class': 'w-full px-4 py-3 rounded-lg bg-slate-900 border border-slate-700 text-white focus:outline-none focus:border-brand-gold',
                'placeholder': 'How can we help you today?'
            }),
        }

    def clean_phone(self):
        phone = self.cleaned_data.get('phone')
        if phone:
            cleaned_phone = ''.join(char for char in phone if char.isdigit())
            if len(cleaned_phone) < 10 or len(cleaned_phone) > 12:
                raise forms.ValidationError("Please enter a valid phone number.")
            return cleaned_phone
        return phone


from django.contrib.auth.models import User
from salon.models import UserProfile

class UserSignupForm(forms.ModelForm):
    phone_number = forms.CharField(
        max_length=15,
        widget=forms.TextInput(attrs={
            'class': 'w-full px-4 py-3 rounded-lg bg-slate-900 border border-slate-700 text-white focus:outline-none focus:border-brand-gold',
            'placeholder': 'Phone Number (e.g. 9740637692)'
        })
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'w-full px-4 py-3 rounded-lg bg-slate-900 border border-slate-700 text-white focus:outline-none focus:border-brand-gold',
            'placeholder': 'Choose Password'
        })
    )
    confirm_password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'w-full px-4 py-3 rounded-lg bg-slate-900 border border-slate-700 text-white focus:outline-none focus:border-brand-gold',
            'placeholder': 'Confirm Password'
        })
    )

    class Meta:
        model = User
        fields = ['username', 'email', 'password']
        widgets = {
            'username': forms.TextInput(attrs={
                'class': 'w-full px-4 py-3 rounded-lg bg-slate-900 border border-slate-700 text-white focus:outline-none focus:border-brand-gold',
                'placeholder': 'Choose Username'
            }),
            'email': forms.EmailInput(attrs={
                'class': 'w-full px-4 py-3 rounded-lg bg-slate-900 border border-slate-700 text-white focus:outline-none focus:border-brand-gold',
                'placeholder': 'Your Email Address'
            }),
        }

    def clean_phone_number(self):
        phone = self.cleaned_data.get('phone_number')
        if phone:
            cleaned_phone = ''.join(char for char in phone if char.isdigit())
            if len(cleaned_phone) < 10 or len(cleaned_phone) > 12:
                raise forms.ValidationError("Please enter a valid 10 to 12 digit phone number.")
            if UserProfile.objects.filter(phone_number=cleaned_phone).exists():
                raise forms.ValidationError("A user with this phone number already exists.")
            return cleaned_phone
        return phone

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")
        if password and confirm_password and password != confirm_password:
            raise forms.ValidationError("Passwords do not match.")
        return cleaned_data

