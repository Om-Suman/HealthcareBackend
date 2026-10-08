from rest_framework import generics, viewsets
from rest_framework.permissions import AllowAny, IsAuthenticated

from .models import Doctor, Patient, PatientDoctorMapping
from .serializers import DoctorSerializer, PatientDoctorMappingSerializer, PatientSerializer, RegisterSerializer


class RegisterView(generics.CreateAPIView):
    serializer_class = RegisterSerializer
    permission_classes = [AllowAny]


class PatientViewSet(viewsets.ModelViewSet):
    serializer_class = PatientSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Patient.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class DoctorViewSet(viewsets.ModelViewSet):
    serializer_class = DoctorSerializer
    permission_classes = [IsAuthenticated]
    queryset = Doctor.objects.all()

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def perform_update(self, serializer):
        if serializer.instance.user_id != self.request.user.id:
            from rest_framework.exceptions import PermissionDenied
            raise PermissionDenied("You can only update doctors you created.")
        serializer.save()

    def perform_destroy(self, instance):
        if instance.user_id != self.request.user.id:
            from rest_framework.exceptions import PermissionDenied
            raise PermissionDenied("You can only delete doctors you created.")
        instance.delete()


class MappingViewSet(viewsets.ModelViewSet):
    serializer_class = PatientDoctorMappingSerializer
    permission_classes = [IsAuthenticated]
    http_method_names = ["get", "post", "delete", "head", "options"]

    def get_queryset(self):
        if getattr(self, "action", None) == "destroy":
            return PatientDoctorMapping.objects.select_related("patient", "doctor")
        queryset = PatientDoctorMapping.objects.filter(patient__user=self.request.user).select_related("patient", "doctor")
        patient_id = self.kwargs.get("patient_id")
        return queryset.filter(patient_id=patient_id) if patient_id else queryset

    def get_object(self):
        # The assignment specifies GET /mappings/<patient_id>/ and
        # DELETE /mappings/<mapping_id>/, so the integer has a method-specific meaning.
        if "patient_id" in self.kwargs:
            from rest_framework.generics import get_object_or_404
            return get_object_or_404(self.get_queryset(), pk=self.kwargs["patient_id"])
        return super().get_object()

    def perform_destroy(self, instance):
        if instance.patient.user_id != self.request.user.id:
            from rest_framework.exceptions import PermissionDenied
            raise PermissionDenied("You can only remove mappings for your own patients.")
        instance.delete()
