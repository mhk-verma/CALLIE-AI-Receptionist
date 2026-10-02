from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .models import Business, BusinessHours, ReceptionistConfig, EscalationConfig
from .serializers import (
    BusinessSerializer, BusinessHoursSerializer, 
    ReceptionistConfigSerializer, EscalationConfigSerializer
)


class BusinessListAPIView(generics.ListCreateAPIView):
    """API endpoint for listing and creating businesses."""
    serializer_class = BusinessSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Business.objects.filter(owner=self.request.user)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class BusinessDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    """API endpoint for business details."""
    serializer_class = BusinessSerializer
    permission_classes = [IsAuthenticated]
    lookup_field = 'pk'

    def get_queryset(self):
        return Business.objects.filter(owner=self.request.user)


class BusinessHoursAPIView(generics.RetrieveUpdateAPIView):
    """API endpoint for business hours."""
    serializer_class = BusinessHoursSerializer
    permission_classes = [IsAuthenticated]
    lookup_field = 'pk'

    def get_object(self):
        business = generics.get_object_or_404(Business, pk=self.kwargs['pk'], owner=self.request.user)
        return business.business_hours.all()

    def get(self, request, *args, **kwargs):
        business = generics.get_object_or_404(Business, pk=self.kwargs['pk'], owner=self.request.user)
        hours = business.business_hours.all()
        serializer = BusinessHoursSerializer(hours, many=True)
        return Response(serializer.data)

    def put(self, request, *args, **kwargs):
        business = generics.get_object_or_404(Business, pk=self.kwargs['pk'], owner=self.request.user)
        
        # Delete existing hours
        business.business_hours.all().delete()
        
        # Create new hours from request data
        hours_data = request.data.get('hours', [])
        for hour_data in hours_data:
            BusinessHours.objects.create(business=business, **hour_data)
        
        return Response({'message': 'Business hours updated successfully'})


class ReceptionistConfigAPIView(generics.RetrieveUpdateAPIView):
    """API endpoint for receptionist configuration."""
    serializer_class = ReceptionistConfigSerializer
    permission_classes = [IsAuthenticated]
    lookup_field = 'pk'

    def get_object(self):
        business = generics.get_object_or_404(Business, pk=self.kwargs['pk'], owner=self.request.user)
        return generics.get_object_or_404(ReceptionistConfig, business=business)


class EscalationConfigAPIView(generics.RetrieveUpdateAPIView):
    """API endpoint for escalation configuration."""
    serializer_class = EscalationConfigSerializer
    permission_classes = [IsAuthenticated]
    lookup_field = 'pk'

    def get_object(self):
        business = generics.get_object_or_404(Business, pk=self.kwargs['pk'], owner=self.request.user)
        return generics.get_object_or_404(EscalationConfig, business=business)
