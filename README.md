# 'D' MAGICAL Family Salon

A premium, luxury family salon booking and management web application built with Python, Django, Tailwind CSS, and SQLite. This application allows clients to view beauty and grooming services, book instant appointments, scan simulated UPI payment QR codes, and provides owners with a secure, login-protected management dashboard.

---

## 🌟 Features

### 1. Client Experience & Services
* **Modern Landing Page**: Clean dark-theme design with high-quality featured services, client testimonials, operational hours, and direct booking triggers.
* **Service & Pricing Menu**: Categorized list of grooming and styling options with duration details.
  * *Classic Haircut* updated to **₹100**.
  * *Classic Shave & Beard Trim* updated to **₹50**.
* **Instant Booking System**: Step-by-step booking form with frontend/backend validation (e.g., date selection limits, formatting checks).
* **Payment Integration**: Supports Cash on Delivery (COD) and simulated UPI Payment (Scan & Pay) with dynamic QR generation based on service price.
* **Customer Inquiries**: Contact page to drop custom messages/inquiries directly to the salon management.

### 2. Management & Administration
* **Multi-Field Authentication**: Secure login supporting registration and sign-in using either **Email Address** or **Phone Number**.
* **Custom Auth Backend**: Utilizes `EmailOrPhoneBackend` to inspect inputs and match against standard user records and linked phone numbers.
* **Locked-down Owner Dashboard**: Restricts access to authenticated users only. Allows owners to:
  * View overall dashboard metrics (Total Appointments, Revenue, Pending Inquiries, Today's Bookings).
  * Confirm or Cancel client bookings with instant status updates.
  * Mark UPI payments as Completed or Failed.
  * Resolve customer inquiries.

---

## 🛠️ Technology Stack
* **Backend**: Django 6.0 (Python)
* **Database**: SQLite3
* **Frontend styling**: Tailwind CSS (CDN implementation with brand configuration), Vanilla CSS
* **Icons & Typography**: FontAwesome 6, Google Fonts (*Playfair Display* & *Inter*)
* **Testing**: Django standard TestCase suite

---

## 🚀 Installation & Local Setup

### 1. Prerequisities
Make sure Python 3.10+ is installed on your machine.

### 2. Set Up Virtual Environment
Activate the pre-configured virtual environment:
```bash
# On Windows PowerShell/CMD:
venv\Scripts\activate

# On macOS/Linux:
source venv/bin/activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Apply Database Migrations
```bash
python manage.py migrate
```

### 5. Seed Services & Owner Account
Seed the standard salon services and the default administrator user:
```bash
python manage.py seed_services
```

---

## 🖥️ Running the Application

### Start Development Server
```bash
python manage.py runserver
```
Once started, navigate to:
* **Salon Website**: [http://127.0.0.1:8000/](http://127.0.0.1:8000/)
* **Services & Pricing**: [http://127.0.0.1:8000/services/](http://127.0.0.1:8000/services/)
* **Secure Owner Dashboard**: [http://127.0.0.1:8000/dashboard/](http://127.0.0.1:8000/dashboard/)

---

## 🔑 Seeded Owner Account (For Testing)
You can access the locked-down dashboard using either of the following credentials:
* **Sign In via Email**: `owner@dmagicalsalon.com`
* **Sign In via Phone**: `9740637692`
* **Password**: `magicalpassword123`

---

## 🧪 Running Unit Tests
To verify all models, forms, custom login handlers, and route protections:
```bash
python manage.py test
```
*(All 14 tests should run and pass successfully)*
