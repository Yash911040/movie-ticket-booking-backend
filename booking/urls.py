from django.urls import path
from .views import BookSeatView, CancelBookingView, MyBookingsView
from .views import (
    SignupView,
    LoginView,
    MovieListView,
    ShowListView,
)

urlpatterns = [
    path('signup/', SignupView.as_view()),
    path('login/', LoginView.as_view()),
    path('movies/', MovieListView.as_view()),
    path('movies/<int:id>/shows/', ShowListView.as_view()),
]
urlpatterns += [
    path('shows/<int:id>/book/', BookSeatView.as_view()),
    path('bookings/<int:id>/cancel/', CancelBookingView.as_view()),
    path('my-bookings/', MyBookingsView.as_view()),
]
