from django.urls import include, path
from rest_framework.routers import SimpleRouter

from .views import DoctorViewSet, MappingViewSet, PatientViewSet

router = SimpleRouter()
router.register("patients", PatientViewSet, basename="patient")
router.register("doctors", DoctorViewSet, basename="doctor")
router.register("mappings", MappingViewSet, basename="mapping")

urlpatterns = [
    path("mappings/<int:patient_id>/", MappingViewSet.as_view({"get": "list", "delete": "destroy"}), name="patient-mappings"),
    path("", include(router.urls)),
]
