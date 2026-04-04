from rest_framework import serializers
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model

from .models import Cart, Customer, Menu, Order, OrderItem, Reservation, Review, Special

# Get all menu
class MenuSerializer(serializers.ModelSerializer):
    class Meta:
        model = Menu
        fields = '__all__'

# Get all customer
User = get_user_model()

class UserShortSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        # Only include the basic user info you want to show
        fields = ['id', 'username', 'first_name', 'last_name', 'email']

class CustomerSerializer(serializers.ModelSerializer):
    user = UserShortSerializer(read_only=True)
    class Meta:
        model = Customer
        fields = ['id', 'user', 'phone', 'address', 'created_at']

# Register
class UserRegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True) # Don't show password in response
    class Meta:
        model = User
        fields = ['id', 'username', 'password', 'first_name', 'last_name', 'email']

class CustomerRegisterSerializer(serializers.ModelSerializer):
    user = UserRegisterSerializer()
    id = serializers.IntegerField(read_only=True)
    class Meta:
        model = Customer
        fields = ['id', 'user', 'phone', 'address']

    def create(self, validated_data):
        user_data = validated_data.pop('user')
        user = User.objects.create_user(**user_data)
        customer = Customer.objects.create(user=user, **validated_data)
        return customer

# Update customer
class UserUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']

class CustomerUpdateSerializer(serializers.ModelSerializer):
    user = UserUpdateSerializer()
    class Meta:
        model = Customer
        fields = ['user', 'phone', 'address']

    def update(self, instance, validated_data):
        user_data = validated_data.pop('user', None)
        if user_data:
            user_serializer = UserUpdateSerializer(instance.user, data=user_data, partial=True)
            if user_serializer.is_valid():
                user_serializer.save()

        instance.phone = validated_data.get('phone', instance.phone)
        instance.address = validated_data.get('address', instance.address)
        instance.save()
        
        return instance
    
# reviews
class ReviewSerializer(serializers.ModelSerializer):
    menu_name = serializers.ReadOnlyField(source='menu.name')
    class Meta:
        model = Review
        fields = ['id', 'menu_id', 'menu_name', 'rating', 'comment', 'created_at']

class ReviewUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        # We only allow updating the rating and comment
        fields = ['rating', 'comment']

# orders
class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ['id', 'total_price', 'status', 'order_date']

class OrderItemSerializer(serializers.ModelSerializer):
    menu_name = serializers.ReadOnlyField(source='menu.name')
    subtotal = serializers.ReadOnlyField() 
    class Meta:
        model = OrderItem
        fields = ['id', 'menu_id', 'menu_name', 'quantity', 'price', 'subtotal']

# reservation
class ReservationSerializer(serializers.ModelSerializer):
    phone = serializers.ReadOnlyField(source='customer.phone')
    first_name = serializers.ReadOnlyField(source='customer.user.first_name')
    last_name = serializers.ReadOnlyField(source='customer.user.last_name')
    class Meta:
        model = Reservation
        fields = ['id', 'first_name', 'last_name', 'phone', 'status', 'reservation_date', 'reservation_time', 'party_size', 'seating_choice', 'allergy_info']

class ReservationCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reservation
        fields = ['reservation_date', 'reservation_time', 'party_size', 'seating_choice', 'allergy_info']

    def validate_party_size(self, value):
        if value < 1:
            raise serializers.ValidationError("Party size must be at least 1.")
        return value
    

# Ordering - checkout system
class CartItemInputSerializer(serializers.Serializer):
    menu_id = serializers.IntegerField()
    quantity = serializers.IntegerField(min_value=1)

class CheckoutSessionSerializer(serializers.Serializer):
    items = CartItemInputSerializer(many=True)