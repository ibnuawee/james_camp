from django.db import models
from django.contrib.auth import get_user_model
import uuid

User = get_user_model()

class PaymentMethod(models.Model):
    name = models.CharField(max_length=100, unique=True)  # Nama metode pembayaran
    description = models.TextField(blank=True, null=True)  # Deskripsi metode pembayaran
    is_active = models.BooleanField(default=True)  # Hanya metode pembayaran aktif yang dapat digunakan

    def __str__(self):
        return self.name

class Transaction(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('paid', 'Paid'),
        ('processing', 'Processing'),
        ('success', 'Success'),
        ('canceled', 'Canceled'),
    ]

    invoice_id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)  # Invoice ID otomatis
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='transactions')
    item = models.ForeignKey('camping.CampingItem', on_delete=models.CASCADE, related_name='transactions')
    quantity = models.PositiveIntegerField()
    total_price = models.DecimalField(max_digits=12, decimal_places=2, blank=True, null=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')
    rent_date = models.DateField(null=True, blank=True)
    return_date = models.DateField(null=True, blank=True)
    identity_photo = models.ImageField(upload_to='identity_photos/', blank=True, null=True)
    payment_method = models.ForeignKey(PaymentMethod, on_delete=models.SET_NULL, null=True, blank=True)
    note = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        if self.rent_date and self.return_date:
            days_rented = (self.return_date - self.rent_date).days
        else:
            days_rented = 1  # Default ke 1 hari jika salah satu tanggal tidak ada

            # Hitung total harga berdasarkan jumlah barang, harga per item, dan jumlah hari
        self.total_price = self.quantity * self.item.price * days_rented

        # Handle stock adjustments
        if self.pk:  # Check if the transaction already exists (update case)
            original = Transaction.objects.get(pk=self.pk)
            if original.status == 'pending' and self.status in ['paid', 'processing']:
                if self.quantity > self.item.stock:
                    raise ValueError("Stok barang tidak mencukupi.")
                self.item.stock -= self.quantity
                self.item.save()

            if original.status == 'processing' and self.status == 'success':
                # Return stock if transaction is marked as success
                self.item.stock += self.quantity
                self.item.save()
        else:  # New transaction
            if self.status in ['processing', 'paid']:
                # Decrease stock on new transaction
                self.item.stock -= self.quantity
                self.item.save()
        super().save(*args, **kwargs)
