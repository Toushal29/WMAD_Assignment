# C:\Users\...\WMAD_Assignment\WMAD_project\web_app\serializers.py

# These serializers handle data conversion, validation and specify which fields are included in the API responses.

from rest_framework import serializers
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
from .models import Cart, Customer, Menu, Order, OrderItem, Reservation, Review

# convert Menu model instances to JSON and vice versa, including all fields from the Menu model
class MenuSerializer(serializers.ModelSerializer):
    class Meta:
        model = Menu
        fields = '__all__'

# handle user registration, profile retrieval, and profile updates, including nested serialization for the related User model to manage authentication and user details
User = get_user_model()

# serializer for the User model to include only essential fields when nested within the CustomerSerializer
class UserShortSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        # exclude password and other sensitive fields, only include basic user information for display purposes
        fields = ['id', 'username', 'first_name', 'last_name', 'email']

# Serializer for the Customer model that includes a nested UserShortSerializer to represent the related User object
class CustomerSerializer(serializers.ModelSerializer):
    user = UserShortSerializer(read_only=True)
    class Meta:
        model = Customer
        fields = ['id', 'user', 'phone', 'address', 'created_at']

# Serializer for user registration that includes a nested UserRegisterSerializer to handle the creation of the related User object
class UserRegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True) # Don't show password in response
    class Meta:
        model = User
        fields = ['id', 'username', 'password', 'first_name', 'last_name', 'email']

# Serializer for customer registration that includes a nested UserRegisterSerializer to handle the creation of the related User object
class CustomerRegisterSerializer(serializers.ModelSerializer):
    user = UserRegisterSerializer()         # This allows us to create a User object when registering a new Customer
    id = serializers.IntegerField(read_only=True)
    class Meta:
        model = Customer
        fields = ['id', 'user', 'phone', 'address']

    # Override the create method to handle the creation of the User object when a new Customer is registered
    def create(self, validated_data):
        user_data = validated_data.pop('user')
        user = User.objects.create_user(**user_data)
        customer = Customer.objects.create(user=user, **validated_data)
        return customer

# Serializer for updating the User model, allowing for updates to the user's first name, last name, and email while keeping the password and username unchanged
class UserUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'first_name', 'last_name', 'email']


# Serializer for updating the Customer model that includes a nested UserUpdateSerializer to handle updates to the related User object, allowing profile update process where both the customer's personal details and their information can be updated in a single API request
class CustomerUpdateSerializer(serializers.ModelSerializer):
    user = UserUpdateSerializer(partial=True)       # Allow partial updates to the nested User object of fields
    class Meta:
        model = Customer
        fields = ['id', 'user', 'phone', 'address']

    def update(self, instance, validated_data):             # Handle the nested user data update
        user_data = validated_data.pop('user', None)        # Extract the nested user data if it exists
        if user_data:
            user_serializer = UserUpdateSerializer(instance.user, data=user_data, partial=True)
            user_serializer.is_valid(raise_exception=True)
            user_serializer.save()
        
        # Update the customer fields (phone, address)
        return super().update(instance, validated_data)



# Serializer for the Review model for the creation and updating of reviews based on the menu ID, rating, comment, and created_at timestamp
class ReviewSerializer(serializers.ModelSerializer):
    menu_name = serializers.ReadOnlyField(source='menu.name')       # This provides the name of the dish for the frontend, but is read-only
    class Meta:
        model = Review
        fields = ['id', 'menu', 'menu_name', 'rating', 'comment', 'created_at']


# Separate serializers for creating and updating reviews to handle different validation requirements like ensuring that the rating is between 1 and 5 when creating a review
class ReviewCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = ['menu', 'rating', 'comment']

    def validate_rating(self, value):
        if value < 1 or value > 5:
            raise serializers.ValidationError("Rating must be between 1 and 5.")
        return value


# Serializer for updating reviews that allows for partial updates to the rating and comment fields
class ReviewUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        # allow updating the rating and comment
        fields = ['rating', 'comment']

# Serializer for the Order model that includes fields for the total price, status, payment method, and order date
class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ['id', 'total_price', 'status', 'payment_method', 'order_date']

# Serializer for the OrderItem model that includes read-only fields for the menu name and subtotal, menu item and the calculated subtotal for line item without requiring additional API calls to retrieve that information
class OrderItemSerializer(serializers.ModelSerializer):
    menu_name = serializers.ReadOnlyField(source='menu.name')
    subtotal = serializers.ReadOnlyField() 
    class Meta:
        model = OrderItem
        fields = ['id', 'menu_id', 'menu_name', 'quantity', 'price', 'subtotal']

# Serializer for the Reservation model that includes read-only fields for the customer's phone number and name
class ReservationSerializer(serializers.ModelSerializer):
    phone = serializers.ReadOnlyField(source='customer.phone')
    first_name = serializers.ReadOnlyField(source='customer.user.first_name')
    last_name = serializers.ReadOnlyField(source='customer.user.last_name')
    class Meta:
        model = Reservation
        fields = ['id', 'first_name', 'last_name', 'phone', 'status', 'reservation_date', 'reservation_time', 'party_size', 'seating_choice', 'allergy_info']

# Separate serializer for creating reservations that includes validation for the party size to ensure it is at least 1
class ReservationCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reservation
        fields = ['reservation_date', 'reservation_time', 'party_size', 'seating_choice', 'allergy_info']

    def validate_party_size(self, value):
        if value < 1:
            raise serializers.ValidationError("Party size must be at least 1.")
        return value


# Serializer for adding items to the cart that includes fields for the menu ID and quantity, allowing the frontend to send the necessary data to add items to the cart
class CartItemInputSerializer(serializers.Serializer):
    menu_id = serializers.IntegerField()
    quantity = serializers.IntegerField(min_value=1)

# Serializer for the checkout session that includes a list of cart items and a payment method choice
class CheckoutSessionSerializer(serializers.Serializer):
    items = CartItemInputSerializer(many=True)
    # payment choice during checkout
    payment_method = serializers.ChoiceField(choices=Order.PAYMENT_CHOICES, default=Order.PAYMENT_CASH)


# Serializer for adding items to the cart
class addCartSerializer(serializers.ModelSerializer):
    # This provides the name of the dish for the frontend, but is read-only
    menu_name = serializers.ReadOnlyField(source='menu.name')

    class Meta:
        model = Cart
        # These fields are based on the Cart and Menu models
        fields = ['id', 'menu', 'menu_name', 'quantity', 'added_at']


# Serializer for the Cart model that includes read-only fields for the menu name, price, and a method field to calculate the subtotal for each cart item, allowing the frontend to display detailed information about the items in the cart without needing additional API calls to retrieve that information
class CartSerializer(serializers.ModelSerializer):
    menu_name = serializers.ReadOnlyField(source='menu.name')       # Pulling readable details from the related Menu model
    price = serializers.ReadOnlyField(source='menu.price')
    subtotal = serializers.SerializerMethodField()              # Calculating the subtotal for this specific cart item

    class Meta:
        model = Cart
        # These fields are based on the Cart and Menu models in your sources
        fields = ['id', 'menu', 'menu_name', 'quantity', 'price', 'subtotal', 'added_at']

    def get_subtotal(self, obj):        # This method calculates the subtotal for a cart item by multiplying the quantity of the item in the cart by the price of the menu item
        return obj.quantity * obj.menu.price