from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.http import HttpResponseRedirect, JsonResponse
from salon.models import Service, Appointment, Inquiry, UserProfile
from salon.forms import AppointmentForm, InquiryForm, UserSignupForm
from django.utils import timezone
from django.db.models import Sum

def home(request):
    featured_services = Service.objects.filter(is_featured=True)[:6]
    context = {
        'featured_services': featured_services,
    }
    return render(request, 'salon/home.html', context)


def services(request):
    all_services = Service.objects.all()
    categories = Service.CATEGORY_CHOICES
    
    # Group services by category for easier template rendering
    grouped_services = {}
    for code, label in categories:
        services_in_cat = all_services.filter(category=code)
        if services_in_cat.exists():
            grouped_services[label] = services_in_cat
            
    context = {
        'grouped_services': grouped_services,
    }
    return render(request, 'salon/services.html', context)


def booking(request):
    if request.method == 'POST':
        form = AppointmentForm(request.POST)
        if form.is_valid():
            appointment = form.save(commit=False)
            
            # Additional booking validation/processing
            appointment.booking_status = 'PENDING'
            appointment.payment_status = 'PENDING'
            appointment.save()
            
            # Store in session to display payment screen or confirmation
            request.session['latest_appointment_id'] = appointment.id
            
            if appointment.payment_method == 'UPI':
                return redirect('payment_upi')
            else:
                messages.success(request, f"Thank you, {appointment.customer_name}! Your booking for {appointment.service.name} has been received and is pending confirmation.")
                return redirect('booking_success')
        else:
            messages.error(request, "Please correct the errors in the booking form.")
    else:
        # Check if service ID was passed as a query param (e.g. from Home page or Services page)
        initial_data = {}
        service_id = request.GET.get('service')
        if service_id:
            try:
                initial_data['service'] = Service.objects.get(id=service_id)
            except Service.DoesNotExist:
                pass
        form = AppointmentForm(initial=initial_data)

    context = {
        'form': form,
    }
    return render(request, 'salon/booking.html', context)


def payment_upi(request):
    appointment_id = request.session.get('latest_appointment_id')
    if not appointment_id:
        return redirect('booking')
        
    appointment = get_object_or_404(Appointment, id=appointment_id)
    
    if request.method == 'POST':
        # Simulate user confirming they made the UPI payment
        appointment.payment_status = 'PENDING'  # Salon owner will verify and mark as completed
        appointment.save()
        messages.success(request, f"Thank you, {appointment.customer_name}! We have logged your UPI payment request. We will confirm your booking once verified.")
        return redirect('booking_success')
        
    # Generate UPI URI for QR code (simulated)
    # Format: upi://pay?pa=recipient@upi&pn=RecipientName&am=Amount&cu=INR
    upi_pa = "9740637692@okbizaxis" # Simulated salon UPI ID using contact number
    upi_pn = "D Magical Family Salon"
    upi_am = str(appointment.service.price)
    upi_uri = f"upi://pay?pa={upi_pa}&pn={upi_pn}&am={upi_am}&cu=INR"
    
    context = {
        'appointment': appointment,
        'upi_uri': upi_uri,
        'upi_id': upi_pa,
    }
    return render(request, 'salon/payment_upi.html', context)


def booking_success(request):
    appointment_id = request.session.get('latest_appointment_id')
    if not appointment_id:
        return redirect('home')
        
    appointment = get_object_or_404(Appointment, id=appointment_id)
    context = {
        'appointment': appointment,
    }
    return render(request, 'salon/booking_success.html', context)


def contact(request):
    if request.method == 'POST':
        form = InquiryForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Your inquiry has been submitted successfully! We will contact you soon.")
            return redirect('contact')
        else:
            messages.error(request, "Please correct the errors in the contact form.")
    else:
        form = InquiryForm()
        
    context = {
        'form': form,
    }
    return render(request, 'salon/contact.html', context)


@login_required(login_url='login')
def dashboard(request):
    # Retrieve filtering or sorting parameters if any
    appointments = Appointment.objects.all().order_by('-date', '-time')
    inquiries = Inquiry.objects.all().order_by('is_resolved', '-created_at')
    services = Service.objects.all().order_by('category', 'name')
    
    # Analytics / Dashboard metrics
    today = timezone.localdate()
    stats = {
        'total_appointments': appointments.count(),
        'pending_appointments': appointments.filter(status='PENDING').count(),
        'confirmed_appointments': appointments.filter(status='CONFIRMED').count(),
        'total_inquiries': inquiries.count(),
        'pending_inquiries': inquiries.filter(is_resolved=False).count(),
        'total_revenue': appointments.filter(payment_status='COMPLETED').aggregate(Sum('service__price'))['service__price__sum'] or 0.00,
        'today_bookings': appointments.filter(date=today).count(),
    }
    
    context = {
        'appointments': appointments,
        'inquiries': inquiries,
        'services': services,
        'stats': stats,
    }
    return render(request, 'salon/dashboard.html', context)


# Admin action views

@login_required(login_url='login')
def update_appointment_status(request, pk, status):
    appointment = get_object_or_404(Appointment, id=pk)
    if status in ['PENDING', 'CONFIRMED', 'CANCELLED']:
        appointment.status = status
        appointment.save()
        messages.success(request, f"Appointment for {appointment.customer_name} updated to {status.capitalize()}.")
    return redirect('dashboard')


@login_required(login_url='login')
def update_payment_status(request, pk, status):
    appointment = get_object_or_404(Appointment, id=pk)
    if status in ['PENDING', 'COMPLETED', 'FAILED']:
        appointment.payment_status = status
        # Auto-confirm booking if payment is marked completed
        if status == 'COMPLETED' and appointment.status == 'PENDING':
            appointment.status = 'CONFIRMED'
        appointment.save()
        messages.success(request, f"Payment status for {appointment.customer_name} updated to {status.capitalize()}.")
    return redirect('dashboard')


@login_required(login_url='login')
def resolve_inquiry(request, pk):
    inquiry = get_object_or_404(Inquiry, id=pk)
    inquiry.is_resolved = True
    inquiry.save()
    messages.success(request, f"Inquiry from {inquiry.name} marked as resolved.")
    return redirect('dashboard')


def login_view(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
        
    if request.method == 'POST':
        identifier = request.POST.get('username')
        password = request.POST.get('password')
        
        if not identifier or not password:
            messages.error(request, "Please enter all fields.")
        else:
            user = authenticate(request, username=identifier, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, f"Welcome back, {user.username}!")
                next_url = request.GET.get('next')
                if next_url:
                    return redirect(next_url)
                return redirect('dashboard')
            else:
                messages.error(request, "Invalid credentials. Please verify email/phone and password.")
    
    return render(request, 'salon/login.html')


def signup_view(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
        
    if request.method == 'POST':
        form = UserSignupForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.save()
            
            # Create UserProfile
            phone_number = form.cleaned_data['phone_number']
            UserProfile.objects.create(user=user, phone_number=phone_number)
            
            # Log the user in using default backend
            login(request, user, backend='django.contrib.auth.backends.ModelBackend')
            messages.success(request, f"Registration successful! Welcome, {user.username}!")
            return redirect('dashboard')
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"{field.capitalize()}: {error}")
    else:
        form = UserSignupForm()
        
    return render(request, 'salon/signup.html', {'form': form})


def logout_view(request):
    logout(request)
    messages.success(request, "Successfully logged out.")
    return redirect('home')
