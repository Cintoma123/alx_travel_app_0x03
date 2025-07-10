from django.shortcuts import render
from rest_framework import serializers, viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from listings.models import Listing, Booking
from listings.serializers import ListingSerializer, BookingSerializer
from listings.tasks import send_email_message


"""class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    lookup_field = 'id'"""


class BookingViewSet(viewsets.ModelViewSet):
    serializer_class = BookingSerializer
    queryset = Booking.objects.all()

    @action(detail=False, methods=['post'])
    def email_message_post(self, request):
        serializer = BookingSerializer(data=request.data)
        try:
            serializer.is_valid(raise_exception=True)
            serializer.save()

            validated_data = serializer.validated_data
            send_email_message.delay(
                validated_data['sender'],
                validated_data['receiver'],
                validated_data['message']
            )

            return Response(
                {'status': 'success', 'message': 'Email sent successfully'},
                status=status.HTTP_201_CREATED
            )
        except serializers.ValidationError as e:
            return Response(
                {'status': 'error', 'message': str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )


class ListingViewSet(viewsets.ModelViewSet):
    serializer_class = ListingSerializer
    queryset = Listing.objects.all()
    permission_classes = [IsAuthenticated]

    @action(detail=False, methods=['post'])
    def list_made_by_user(self, request):
        serializer = ListingSerializer(data=request.data, many=True)
        if serializer.is_valid():
            user = request.user
            # Assuming make_list is a custom method on the User model
            user.make_list(serializer.validated_data)
            user.save()
            return Response(
                {'status': 'success', 'message': 'Listings created successfully'},
                status=status.HTTP_201_CREATED
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['get'])
    def retrieve_bookings_made_by_user(self, request, pk=None):
        user = self.get_object()
        bookings = Booking.objects.filter(user_id=user.id)
        serializer = BookingSerializer(bookings, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(detail=True, methods=['put'])
    def updated_bookings_made_by_user(self, request, pk=None):
        user = self.get_object()
        bookings = Booking.objects.filter(user_id=user.id)
        serializer = BookingSerializer(bookings, data=request.data, many=True)
        if serializer.is_valid():
            serializer.save()
            return Response(
                {'status': 'success', 'message': 'Bookings updated successfully'},
                status=status.HTTP_200_OK
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['delete'])
    def delete_bookings_made_by_user(self, request, pk=None):
        user = self.get_object()
        bookings = Booking.objects.filter(user_id=user.id)
        if bookings.exists():
            bookings.delete()
            return Response(
                {'status': 'success', 'message': 'Bookings deleted successfully'},
                status=status.HTTP_204_NO_CONTENT
            )
        return Response(
            {'status': 'error', 'message': 'No bookings found for this user'},
            status=status.HTTP_404_NOT_FOUND
        )
