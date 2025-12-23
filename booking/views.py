from drf_yasg.utils import swagger_auto_schema
from django.contrib.auth.models import User
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.generics import ListAPIView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from drf_yasg import openapi


from .models import Movie, Show, Booking

from .serializers import (
    SignupSerializer,
    MovieSerializer,
    ShowSerializer,
    BookingSerializer,
    LoginSerializer
)


# ---------------- AUTH APIs ----------------

class SignupView(APIView):
    permission_classes = [AllowAny]

    @swagger_auto_schema(request_body=SignupSerializer)
    def post(self, request):
        serializer = SignupSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(
                {"message": "User created successfully"},
                status=status.HTTP_201_CREATED
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



from .serializers import LoginSerializer

class LoginView(APIView):
    permission_classes = [AllowAny]

    @swagger_auto_schema(request_body=LoginSerializer)
    def post(self, request):
        username = request.data.get("username")
        password = request.data.get("password")

        user = User.objects.filter(username=username).first()

        if user and user.check_password(password):
            refresh = RefreshToken.for_user(user)
            return Response({
                "access": str(refresh.access_token),
                "refresh": str(refresh)
            })

        return Response(
            {"error": "Invalid credentials"},
            status=status.HTTP_401_UNAUTHORIZED
        )


# ---------------- MOVIE & SHOW APIs ----------------

class MovieListView(ListAPIView):
    queryset = Movie.objects.all()
    serializer_class = MovieSerializer
    permission_classes = [AllowAny]


class ShowListView(ListAPIView):
    serializer_class = ShowSerializer
    permission_classes = [AllowAny]

    def get_queryset(self):
        movie_id = self.kwargs['id']
        return Show.objects.filter(movie_id=movie_id)
class BookSeatView(APIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            required=['seat_number'],
            properties={
                'seat_number': openapi.Schema(
                    type=openapi.TYPE_INTEGER,
                    description='Seat number to book'
                )
            }
        )
    )
    def post(self, request, id):
        show = get_object_or_404(Show, id=id)
        seat_number = request.data.get("seat_number")

        if not seat_number:
            return Response(
                {"error": "seat_number is required"},
                status=status.HTTP_400_BAD_REQUEST
            )

        if int(seat_number) < 1 or int(seat_number) > show.total_seats:
            return Response(
                {"error": "Invalid seat number"},
                status=status.HTTP_400_BAD_REQUEST
            )

        if Booking.objects.filter(
            show=show,
            seat_number=seat_number,
            status='booked'
        ).exists():
            return Response(
                {"error": "Seat already booked"},
                status=status.HTTP_400_BAD_REQUEST
            )

        booked_count = Booking.objects.filter(
            show=show,
            status='booked'
        ).count()

        if booked_count >= show.total_seats:
            return Response(
                {"error": "Show is fully booked"},
                status=status.HTTP_400_BAD_REQUEST
            )

        booking = Booking.objects.create(
            user=request.user,
            show=show,
            seat_number=seat_number,
            status='booked'
        )

        return Response(
            BookingSerializer(booking).data,
            status=status.HTTP_201_CREATED
        )

class CancelBookingView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, id):
        booking = get_object_or_404(Booking, id=id, user=request.user)

        if booking.status == 'cancelled':
            return Response(
                {"error": "Booking already cancelled"},
                status=status.HTTP_400_BAD_REQUEST
            )

        booking.status = 'cancelled'
        booking.save()

        return Response(
            {"message": "Booking cancelled successfully"},
            status=status.HTTP_200_OK
        )
class MyBookingsView(ListAPIView):
    serializer_class = BookingSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Booking.objects.filter(
            user=self.request.user,
            status='booked'
        )


def get_queryset(self):
    status_param = self.request.query_params.get('status')

    qs = Booking.objects.filter(user=self.request.user)

    if status_param:
        qs = qs.filter(status=status_param)
    else:
        qs = qs.filter(status='booked')

    return qs


