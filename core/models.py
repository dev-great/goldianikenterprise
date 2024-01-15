import uuid
from django.db import models
from django.utils import timezone
from django.contrib.auth import get_user_model
from cloudinary.models import CloudinaryField

CustomUser = get_user_model()


class Tag(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Meal(models.Model):
    id = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False, unique=True, db_index=True)
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=8, decimal_places=2)
    tag = models.ManyToManyField(Tag, blank=True, null=True)
    image = CloudinaryField('image')

    def __str__(self):
        return self.name


class ShippingAddress(models.Model):
    id = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False, unique=True, db_index=True)
    user = models.ForeignKey(
        CustomUser, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    phone_number = models.CharField(max_length=20)
    city = models.CharField(max_length=255, blank=True, null=True)
    additional_information = models.TextField(
        blank=True, null=True)
    created_on = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.first_name} {self.last_name} - {self.city}"

    class Meta:
        ordering = ('-created_on',)


class Cart(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4,
                          editable=False, unique=True, db_index=True)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    created_on = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"Cart for {self.user}"


class CartItem(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4,
                          editable=False, unique=True, db_index=True)
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    meal = models.ForeignKey(Meal, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    subtotal = models.DecimalField(max_digits=10, decimal_places=2)
    created_on = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.quantity} x {self.meal.name} in Cart #{self.cart.id}"


class Order(models.Model):
    id = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False, db_index=True)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    address = models.ForeignKey(ShippingAddress, on_delete=models.DO_NOTHING)
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=20, choices=[(
        'pending', 'Pending'), ('completed', 'Completed')])
    created_on = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"Order for {self.user} - Total Price: {self.total_price}"


class OrderItem(models.Model):
    id = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False, unique=True, db_index=True)
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    meal = models.ForeignKey(Meal, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    subtotal = models.DecimalField(max_digits=10, decimal_places=2)
    created_on = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.quantity} x {self.meal.name} in Order #{self.order.id}"


class Testimonial(models.Model):
    author = models.CharField(max_length=255)
    position = models.CharField(max_length=255)
    content = models.TextField()

    def __str__(self):
        return self.author


class Subscriber(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4,
                          editable=False, unique=True, db_index=True)
    email = models.EmailField()
    created_on = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.email}"


class ContactUs(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4,
                          editable=False, unique=True, db_index=True)
    email = models.EmailField()
    name = models.CharField(max_length=255)
    phone_number = models.CharField(max_length=20)
    subject = models.CharField(max_length=255)
    message = models.TextField()
    created_on = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.email}"
