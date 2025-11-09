from django.db import models

class GalleryImage(models.Model):
    title = models.CharField(max_length=100)
    image = models.ImageField(upload_to='gallery/')
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


class Booking(models.Model):

    SERVICE_CHOICES = [
        ("Airport Pickup & Drop", "Airport Pickup & Drop"),
        ("Tirumala Temple Visit", "Tirumala Temple Visit"),
        ("Outstation Trip", "Outstation Trip"),
        ("City Ride", "City Ride"),
        ("Custom / Other", "Custom / Other"),
    ]

    STATUS_CHOICES = [
        ("Pending", "Pending"),
        ("In Progress", "In Progress"),
        ("Completed", "Completed"),
    ]

    full_name = models.CharField(max_length=120)
    email = models.EmailField(blank=True, null=True)
    phone = models.CharField(max_length=20)
    service = models.CharField(max_length=40, choices=SERVICE_CHOICES)
    pickup = models.CharField(max_length=200)
    drop = models.CharField(max_length=200)
    message = models.TextField(blank=True)

    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="Pending")

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.full_name} • {self.service} • {self.status}"
