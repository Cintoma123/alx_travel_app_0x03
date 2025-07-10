from rest_framework import serializers
from listings.models import Listing, Booking


class ListingSerializer(serializers.ModelSerializer):
    id = serializers.UUIDField(read_only=True)
    created_at = serializers.DateTimeField(read_only=True)
    updated_at = serializers.DateTimeField(read_only=True)
    title = serializers.CharField(max_length=255, required=True)

    class Meta:
        model = Listing
        fields = '__all__'
        read_only_fields = [
            'id', 'created_at', 'updated_at',
            'description', 'is_active', 'price',
            'title', 'ceated_at', 'updated_at'
        ]
        extra_kwargs = {
            'title': {'required': True, 'max_length': 255},
            'description': {'required': True},
            'price': {'required': True, 'max_digits': 10, 'decimal_places': 2},
            'is_active': {'default': True}
        }


class BookingSerializer(serializers.ModelSerializer):
    listings = ListingSerializer(many=True, read_only=True)
    user_id = serializers.PrimaryKeyRelatedField(
        read_only=True, source='user_id.username'
    )
    property_id = serializers.PrimaryKeyRelatedField

    class Meta:
        model = Booking
        fields = '__all__'
        read_only_fields = [
            'booking_id', 'created_at', 'updated_at',
            'status', 'property_id', 'user_id',
            'total_price', 'start_date', 'end_date'
        ]
        extra_kwargs = {
            'property_id': {'required': True},
            'user_id': {'required': True},
            'start_date': {'required': True},
            'end_date': {'required': True},
            'total_price': {'required': True, 'max_digits': 10, 'decimal_places': 2},
            'status': {'default': 'pending'}
        }

    # user making multiple booking
    def create(self, data):
        try:
            user = self.context['request'].user
            if not user.make_multiple_booking:
                raise serializers.ValidationError("Users must make multiple bookings")
            listings = [Listing(user=user, **item) for item in data]
            return Listing.objects.bulk_create(listings)
        except Exception as e:
            raise serializers.ValidationError(str(e))

    def validate(self, data):
        """
        Custom validation to ensure user is authenticated before creating a booking.
        """
        try:
            user = self.context['request'].user
            if not user.is_authenticated:
                raise serializers.ValidationError("User must be authenticated to create a booking.")
        except KeyError:
            raise serializers.ValidationError("User must be authenticated to create a booking.")
        return data
