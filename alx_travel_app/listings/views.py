from django.shortcuts import render
from rest_framework import serializers
from .models import Listing, Booking , User
from .task import send_email_message
from rest_framework import viewsets, status
from .serializers import ListingSerializer , BookingSerializer , UserSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_frameworkk import status
class UserViewset(Viewsets.Modelviewset):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    lookup_field = 'bookings'
    lookup_field = 'listings'

class BookingViewSet(viewsets.ModelViewSet):
    """
    A viewset for viewing and editing user instances.
    """
    serializer_class = BookingSerializer
    queryset = Booking.objects.all()

@action(detail=False, methods=[‘post’])
def post (self ,request):
    user = self.get_objects()
    serializer = self.Userserializer(data=request.data, many=True)
try:
    if serializer.is_valid(raise_exception=True):
        serializer.save()
        sender = serializer.validated_data['sender']
        receiver = serializer.validated_data['receiver']
        message = serializer.validated_data['message']
        send_email_message.delay(sender, receiver, message)
        return Response({'status': 'success', 'message': 'Email sent successfully'}, status=status.HTTP_201_CREATED)
    else:
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    except serializers.ValidationError as e:
        return Response({'status': 'error', 'message': str(e)}, status=status.HTTP_400_BAD_REQUEST)
        


class ListingViewSet(viewsets.ModelViewSet):
    """
    A viewset for viewing and editing user instances.
    """
    serializer_class = ListingSerializer
    queryset = Listing.objects.all()
    permission_classes = [IsAuthenticated]


@action(detail=False, methods=[‘post’])
def list_made_by_user(self, request):
    user = self.get_objects()
    serializer = self.Userserializer(data=request.data, many=True)
if serializer.is_valid():
    user.make_bookings(serializer.validated_data['listings'])

    user.save()
    return Response({status: 'success', 'message': 'listings created successfully'}, status=status.HTTP_201_CREATED)
else:
     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@action(detail= True, methods=['retrieve'])
def retrieve_bookings_made_by_user(self, request,pk=None):
    user = self.get_object()
    bookings = Booking.objects.filter(use_id = user.id)
    serializer = self.UserSerializer(data=request.data, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)

@action(detail = True, methods=['update'])
def updated_bookings_made_by_user(self, request, pk=None):
    user = self.get_object()
    bookings = Booking.objects.filter(user_id = user.id)
    serializer = self.UserSerializer(data=request.data, many=True)
    if serializer.is_valid():
        user.update_bookings(serializer.validated_data['bookings'])
        user.update()
        return Response({'status': 'success', 'message': 'Bookings updated successfully'}, status=status.HTTP_200_OK)
    else:
        return Response(serializer.errors, status=status.HTTP_400_BAD_UPDATE)

@action(detail=True, methods=['destroy'])
def delete_bookings_made_by_user(self, request, pk=None):
    user = self.get_object()
    bookings = Booking.objects.filter(user_id=user.id)
    if bookings.exists():
        bookings.delete()
        return Response({'status': 'success', 'message': 'Bookings deleted successfully'}, status=status.HTTP_204_NO_CONTENT)
    else:
        return Response({'status': 'error', 'message': 'No bookings found for this user'}, status=status.HTTP_404_NOT_FOUND)