from rest_framework import generics
from .models import Vendor, PurchaseOrder
from .serializers import VendorSerializer, PurchaseOrderSerializer
from rest_framework.views import APIView
from rest_framework.response import Response


class VendorPerformanceView(APIView):
    def get(self, request, vendor_id):
        try:
            vendor = Vendor.objects.get(id=vendor_id)
            data = {
                "vendor_id": vendor.id,
                "name": vendor.name,
                "on_time_delivery_rate": vendor.on_time_delivery_rate,
                "quality_rating_avg": vendor.quality_rating_avg,
                "average_response_time": vendor.average_response_time,
                "fulfillment_rate": vendor.fulfillment_rate,
            }
            return Response(data)
        except Vendor.DoesNotExist:
            return Response({"message": "Vendor not found"}, status=404)


class VendorListCreateAPIView(generics.ListCreateAPIView):
    queryset = Vendor.objects.all()
    serializer_class = VendorSerializer


class VendorRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Vendor.objects.all()
    serializer_class = VendorSerializer


class PurchaseOrderListCreateAPIView(generics.ListCreateAPIView):
    queryset = PurchaseOrder.objects.all()
    serializer_class = PurchaseOrderSerializer


class PurchaseOrderRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = PurchaseOrder.objects.all()
    serializer_class = PurchaseOrderSerializer
