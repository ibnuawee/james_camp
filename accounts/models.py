from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    ROLE_CHOICES = [
        ('member', 'Member'),
        ('staff', 'Staff'),
        ('admin', 'Admin'),
    ]
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='member')

    def is_member(self):
        return self.role == 'member'

    def is_staff_user(self):
        return self.role == 'staff'

    def is_admin(self):
        return self.role == 'admin'
