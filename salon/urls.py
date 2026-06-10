from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('services/', views.services, name='services'),
    path('booking/', views.booking, name='booking'),
    path('booking/payment/upi/', views.payment_upi, name='payment_upi'),
    path('booking/success/', views.booking_success, name='booking_success'),
    path('contact/', views.contact, name='contact'),
    
    # Custom Owner Dashboard and quick actions
    path('dashboard/', views.dashboard, name='dashboard'),
    path('dashboard/appointment/<int:pk>/status/<str:status>/', views.update_appointment_status, name='update_appointment_status'),
    path('dashboard/appointment/<int:pk>/payment/<str:status>/', views.update_payment_status, name='update_payment_status'),
    path('dashboard/inquiry/<int:pk>/resolve/', views.resolve_inquiry, name='resolve_inquiry'),
    
    # Custom Authentication
    path('login/', views.login_view, name='login'),
    path('signup/', views.signup_view, name='signup'),
    path('logout/', views.logout_view, name='logout'),
]

