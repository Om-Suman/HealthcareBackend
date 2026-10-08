from django.contrib.auth import password_validation
from rest_framework import serializers

from .models import Doctor, Patient, PatientDoctorMapping, User


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=8, style={"input_type": "password"})

    class Meta:
        model = User
        fields = ("id", "name", "email", "password")
        read_only_fields = ("id",)

    def validate_password(self, value):
        password_validation.validate_password(value)
        return value

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)


class PatientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Patient
        fields = ("id", "name", "age", "gender", "address", "created_at", "updated_at")
        read_only_fields = ("id", "created_at", "updated_at")


class DoctorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Doctor
        fields = ("id", "name", "specialization", "email", "phone", "created_at", "updated_at")
        read_only_fields = ("id", "created_at", "updated_at")


class PatientDoctorMappingSerializer(serializers.ModelSerializer):
    patient_id = serializers.PrimaryKeyRelatedField(source="patient", queryset=Patient.objects.all())
    doctor_id = serializers.PrimaryKeyRelatedField(source="doctor", queryset=Doctor.objects.all())
    doctor = DoctorSerializer(read_only=True)

    class Meta:
        model = PatientDoctorMapping
        fields = ("id", "patient_id", "doctor_id", "doctor", "assigned_at")
        read_only_fields = ("id", "assigned_at")
        validators = []

    def validate(self, attrs):
        request = self.context.get("request")
        patient = attrs.get("patient")
        doctor = attrs.get("doctor")
        if request and patient and patient.user_id != request.user.id:
            raise serializers.ValidationError({"patient_id": "You can only assign doctors to your own patients."})
        if patient and doctor and PatientDoctorMapping.objects.filter(patient=patient, doctor=doctor).exists():
            raise serializers.ValidationError({"doctor_id": "This doctor is already assigned to this patient."})
        return attrs
