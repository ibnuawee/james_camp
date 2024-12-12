from django.db import models
from django.contrib.auth import get_user_model
import uuid

User = get_user_model()

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
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        # Hitung total harga berdasarkan jumlah dan harga per item
        self.total_price = self.quantity * self.item.price

        # Handle stock adjustments
        if self.pk:  # Check if the transaction already exists (update case)
            original = Transaction.objects.get(pk=self.pk)
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
