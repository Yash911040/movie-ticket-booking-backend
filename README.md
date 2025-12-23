# 🎬 Movie Ticket Booking Backend

A Django REST Framework backend for a movie ticket booking system with JWT authentication, seat booking, cancellation, and Swagger API documentation.

## 🚀 Features

- User Signup & Login (JWT Authentication)
- Movie listing
- Show listing per movie
- Seat booking for shows
- Prevention of double booking and overbooking
- Booking cancellation (seat becomes available again)
- User-specific bookings
- Swagger API documentation
- Django Admin Panel

## 🛠️ Tech Stack

- Python 3
- Django
- Django REST Framework
- Simple JWT
- drf-yasg (Swagger)

## ⚙️ Setup Instructions

Clone the repository:
git clone https://github.com/<your-username>/movie-ticket-booking-backend.git
cd movie-ticket-booking-backend

Create virtual environment:
python -m venv venv

Activate virtual environment (Windows):
venv\Scripts\activate

Activate virtual environment (macOS/Linux):
source venv/bin/activate

Install dependencies:
pip install -r requirements.txt

Apply migrations:
python manage.py migrate

Create superuser:
python manage.py createsuperuser

Run server:
python manage.py runserver

## 📘 API Documentation (Swagger)

Open in browser:
http://127.0.0.1:8000/swagger/

## 🔐 Authentication Flow

Signup using /signup/
Login using /login/
Copy JWT access token
Authorize Swagger using:
Bearer <access_token>

## 🎟️ Booking Flow

Admin adds Movies and Shows via admin panel
User books a seat for a show
Seat cannot be double booked
User can cancel booking
Cancelled seats become available again
Users only see active bookings

## 🧪 Testing

APIs tested using Swagger UI and Django Admin Panel
Multi-user booking scenarios tested
Edge cases handled:
- Unauthorized access
- Double booking
- Invalid seat numbers
- Booking cancellation and rebooking

## 👨‍💻 Author

Yavi Kush

## 📄 License

This project is created for learning and assignment purposes.
