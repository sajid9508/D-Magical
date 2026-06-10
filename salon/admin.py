from django.contrib import admin
from .models import Service, Appointment, Inquiry

@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'price', 'duration_minutes', 'is_featured')
    list_filter = ('category', 'is_featured')
    search_fields = ('name', 'description')
    ordering = ('category', 'name')


@admin.register(Appointment)
class AppointmentAdmin(admin.ModelAdmin):
    list_display = ('customer_name', 'service', 'date', 'time', 'payment_method', 'payment_status', 'status')
    list_filter = ('status', 'payment_method', 'payment_status', 'date')
    search_fields = ('customer_name', 'customer_phone', 'customer_email', 'service__name')
    date_hierarchy = 'date'
    ordering = ('date', 'time')


@admin.register(Inquiry)
class InquiryAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'phone', 'is_resolved', 'created_at')
    list_filter = ('is_resolved', 'created_at')
    search_fields = ('name', 'email', 'phone', 'message')
    ordering = ('-created_at',)
