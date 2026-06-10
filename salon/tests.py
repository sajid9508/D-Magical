from django.test import TestCase
from django.urls import reverse
from django.utils import timezone
from salon.models import Service, Appointment, Inquiry
from salon.forms import AppointmentForm, InquiryForm
import datetime

class SalonModelTests(TestCase):
    def setUp(self):
        self.service = Service.objects.create(
            name="Test Cut",
            category="HAIR",
            description="Testing description",
            price=200.00,
            duration_minutes=30,
            is_featured=True
        )

    def test_service_creation(self):
        self.assertEqual(str(self.service), "Test Cut (Hair Grooming & Styling) - ₹200.0")


class SalonFormTests(TestCase):
    def setUp(self):
        self.service = Service.objects.create(
            name="Test Cut",
            category="HAIR",
            description="Testing description",
            price=200.00,
            duration_minutes=30,
            is_featured=True
        )

    def test_appointment_form_valid(self):
        # Tomorrow is a valid date
        tomorrow = timezone.localdate() + datetime.timedelta(days=1)
        form_data = {
            'customer_name': 'Test User',
            'customer_email': 'test@example.com',
            'customer_phone': '9740637692',
            'service': self.service.id,
            'date': tomorrow,
            'time': '14:30',
            'payment_method': 'COD'
        }
        form = AppointmentForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_appointment_form_past_date_invalid(self):
        # Yesterday is an invalid date
        yesterday = timezone.localdate() - datetime.timedelta(days=1)
        form_data = {
            'customer_name': 'Test User',
            'customer_email': 'test@example.com',
            'customer_phone': '9740637692',
            'service': self.service.id,
            'date': yesterday,
            'time': '14:30',
            'payment_method': 'COD'
        }
        form = AppointmentForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('date', form.errors)
        self.assertEqual(form.errors['date'][0], "You cannot book an appointment in the past.")

    def test_appointment_form_future_date_invalid(self):
        # 31 days from now is invalid
        far_future = timezone.localdate() + datetime.timedelta(days=32)
        form_data = {
            'customer_name': 'Test User',
            'customer_email': 'test@example.com',
            'customer_phone': '9740637692',
            'service': self.service.id,
            'date': far_future,
            'time': '14:30',
            'payment_method': 'COD'
        }
        form = AppointmentForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('date', form.errors)
        self.assertEqual(form.errors['date'][0], "Appointments can only be booked up to 30 days in advance.")

    def test_appointment_form_phone_invalid(self):
        tomorrow = timezone.localdate() + datetime.timedelta(days=1)
        form_data = {
            'customer_name': 'Test User',
            'customer_email': 'test@example.com',
            'customer_phone': '12345',  # Too short
            'service': self.service.id,
            'date': tomorrow,
            'time': '14:30',
            'payment_method': 'COD'
        }
        form = AppointmentForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('customer_phone', form.errors)
        self.assertEqual(form.errors['customer_phone'][0], "Please enter a valid 10-digit phone number.")


class SalonViewTests(TestCase):
    def setUp(self):
        self.service = Service.objects.create(
            name="Test Cut",
            category="HAIR",
            description="Testing description",
            price=200.00,
            duration_minutes=30,
            is_featured=True
        )

    def test_home_page_loads(self):
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Where Grooming Meets")

    def test_services_page_loads(self):
        response = self.client.get(reverse('services'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Test Cut")

    def test_contact_page_loads_and_submits(self):
        response = self.client.get(reverse('contact'))
        self.assertEqual(response.status_code, 200)
        
        # Test post submission
        post_data = {
            'name': 'Inquiry Sender',
            'email': 'sender@example.com',
            'phone': '9876543210',
            'message': 'Hello salon team!'
        }
        response = self.client.post(reverse('contact'), data=post_data)
        self.assertEqual(response.status_code, 302) # Redirects back with flash msg
        self.assertEqual(Inquiry.objects.count(), 1)
        self.assertEqual(Inquiry.objects.first().name, 'Inquiry Sender')


from django.contrib.auth.models import User
from salon.models import UserProfile

class SalonAuthTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser",
            email="testuser@example.com",
            password="testpassword123"
        )
        self.profile = UserProfile.objects.create(
            user=self.user,
            phone_number="9999999999"
        )

    def test_login_with_email_success(self):
        login_success = self.client.login(username="testuser@example.com", password="testpassword123")
        self.assertTrue(login_success)

    def test_login_with_phone_success(self):
        login_success = self.client.login(username="9999999999", password="testpassword123")
        self.assertTrue(login_success)

    def test_login_with_username_success(self):
        login_success = self.client.login(username="testuser", password="testpassword123")
        self.assertTrue(login_success)

    def test_login_failure(self):
        login_success = self.client.login(username="testuser", password="wrongpassword")
        self.assertFalse(login_success)

    def test_dashboard_lockdown_redirect(self):
        # Redirect to login if unauthenticated
        response = self.client.get(reverse('dashboard'))
        self.assertEqual(response.status_code, 302)
        self.assertIn('/login/', response.url)

    def test_dashboard_accessible_when_logged_in(self):
        self.client.login(username="testuser", password="testpassword123")
        response = self.client.get(reverse('dashboard'))
        self.assertEqual(response.status_code, 200)

