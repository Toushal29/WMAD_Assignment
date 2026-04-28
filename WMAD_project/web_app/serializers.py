# C:\Users\...\WMAD_Assignment\WMAD_project\web_app\serializers.py

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
        fields = ['id', 'first_name', 'last_name', 'email']

class CustomerUpdateSerializer(serializers.ModelSerializer):
    user = UserUpdateSerializer(partial=True)
    class Meta:
        model = Customer
        fields = ['id', 'user', 'phone', 'address']

    def update(self, instance, validated_data):
        # Handle the nested user data update
        user_data = validated_data.pop('user', None)
        if user_data:
            user_serializer = UserUpdateSerializer(instance.user, data=user_data, partial=True)
            user_serializer.is_valid(raise_exception=True)
            user_serializer.save()
        
        # Update the customer fields (phone, address)
        return super().update(instance, validated_data)
    
# reviews
class ReviewSerializer(serializers.ModelSerializer):
    menu_name = serializers.ReadOnlyField(source='menu.name')
    class Meta:
        model = Review
        # Use 'menu' instead of 'menu_id' to match the model and the JSON body
        fields = ['id', 'menu', 'menu_name', 'rating', 'comment', 'created_at']

class ReviewCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = ['menu', 'rating', 'comment']

    def validate_rating(self, value):
        if value < 1 or value > 5:
            raise serializers.ValidationError("Rating must be between 1 and 5.")
        return value

class ReviewUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        # We only allow updating the rating and comment
        fields = ['rating', 'comment']

# orders
class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ['id', 'total_price', 'status', 'payment_method', 'order_date']

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
    # Add this field to accept the payment choice during checkout
    payment_method = serializers.ChoiceField(choices=Order.PAYMENT_CHOICES, default=Order.PAYMENT_CASH)


####cart creating api

class addCartSerializer(serializers.ModelSerializer):
    # This provides the name of the dish for the frontend, but is read-only
    menu_name = serializers.ReadOnlyField(source='menu.name')

    class Meta:
        model = Cart
        # 'user' is omitted because it will be handled by the view via the Token
        fields = ['id', 'menu', 'menu_name', 'quantity', 'added_at']


class CartSerializer(serializers.ModelSerializer):
    # Pulling readable details from the related Menu model
    menu_name = serializers.ReadOnlyField(source='menu.name')
    price = serializers.ReadOnlyField(source='menu.price')
    
    # Calculating the subtotal for this specific cart item
    subtotal = serializers.SerializerMethodField()

    class Meta:
        model = Cart
        # These fields are based on the Cart and Menu models in your sources
        fields = ['id', 'menu', 'menu_name', 'quantity', 'price', 'subtotal', 'added_at']

    def get_subtotal(self, obj):
        """Calculates the subtotal for the line item."""
        return obj.quantity * obj.menu.price