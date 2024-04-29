from django.db import models
from datetime import datetime, timedelta
import datetime as datetime
from django.utils import timezone
from django.contrib.contenttypes.fields import GenericRelation
from django.db.models import Avg, Count, F, ExpressionWrapper, FloatField
from django.db.models.signals import post_save
from django.dispatch import receiver


class Vendor(models.Model):
    name = models.CharField(max_length=100)
    contact_details = models.TextField()
    address = models.TextField()
    vendor_code = models.CharField(max_length=50, unique=True)
    on_time_delivery_rate = models.FloatField(default=0)
    quality_rating_avg = models.FloatField(default=0)
    average_response_time = models.FloatField(default=0)
    fulfillment_rate = models.FloatField(default=0)

    def __str__(self):
        return self.name

    def calculate_metrics(self):
            # Calculate On-Time Delivery Rate
        total_orders = self.purchaseorder_set.count()
        if total_orders > 0:
            on_time_orders = self.purchaseorder_set.filter(
                status="completed", delivery_date__lte=F("acknowledgment_date")
            ).count()
            self.on_time_delivery_rate = (on_time_orders / total_orders) * 100

            # Calculate Quality Rating Average
        self.quality_rating_avg = (
            self.purchaseorder_set.filter(quality_rating__isnull=False).aggregate(
                avg_rating=Avg("quality_rating")
            )["avg_rating"]
            or 0
        )
            # Calculate average response time
        avg_response_time = self.purchaseorder_set.aggregate(avg_response_time=Avg(F('acknowledgment_date') - F('issue_date')))['avg_response_time']
        
            # Check if avg_response_time is None
        if avg_response_time is None:
            avg_response_time = 0  # Set to zero or another default value
        
            # Convert avg_response_time to timedelta
        avg_response_time = timedelta(seconds=avg_response_time)
        
            # Update vendor metrics
        self.average_response_time = avg_response_time.total_seconds()
        self.save()

            # Calculate Fulfillment Rate
        fulfilled_orders = self.purchaseorder_set.filter(status="completed").count()
        self.fulfillment_rate = (
            (fulfilled_orders / total_orders) * 100 if total_orders > 0 else 0
        )

            # Save the updated metrics
        self.save()


class PurchaseOrder(models.Model):
    STATUS_CHOICES = [
        ("pending", "Pending"),
        ("completed", "Completed"),
        ("canceled", "Canceled"),
    ]

    po_number = models.CharField(max_length=100, unique=True)
    vendor = models.ForeignKey(Vendor, on_delete=models.CASCADE)
    order_date = models.DateTimeField()
    delivery_date = models.DateTimeField()
    items = models.JSONField()
    quantity = models.IntegerField()
    status = models.CharField(max_length=100, choices=STATUS_CHOICES)
    quality_rating = models.FloatField(null=True, blank=True)
    issue_date = models.DateTimeField(auto_now_add=True)
    acknowledgment_date = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return self.po_number


class HistoricalPerformance(models.Model):
    vendor = models.ForeignKey(Vendor, on_delete=models.CASCADE)
    date = models.DateTimeField()
    on_time_delivery_rate = models.FloatField()
    quality_rating_avg = models.FloatField()
    average_response_time = models.FloatField()
    fulfillment_rate = models.FloatField()

    def __str__(self):
        return self.vendor


@receiver(post_save, sender=PurchaseOrder)
def update_vendor_metrics(sender, instance, created, **kwargs):
    if created or instance.vendor:
        instance.vendor.calculate_metrics()
