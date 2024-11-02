import logging
import re
from rest_framework import serializers, validators
from .models import CustomUser,EmployeeProfile,CustomFieldValue
from admin_app.models import Position,CustomField
from admin_app.serializers import CustomFieldValueSerializer


class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ('id', 'email', 'name', 'password', 'is_staff', 'last_login', 'is_active')
        extra_kwargs = {
            'password': {'write_only': True},
            'email': {
                'required': True,
                'allow_blank': False,
                'validators': [
                    validators.UniqueValidator(
                        queryset=CustomUser.objects.all(),
                        message='A user with this email already exists. Please try with another one.'
                    )
                ]
            },
            'is_staff': {'required': False}  # Optional, adjust as needed
        }

    def validate_password(self, value):
        return validation_of_password(value)

    def create(self, validated_data):
        password = validated_data.pop('password', None)

        # Set is_staff to True by default when creating a user
        validated_data['is_staff'] = True

        instance = self.Meta.model(**validated_data)
        if password:
            instance.set_password(password)
        instance.save()
        return instance

    def update(self, instance, validated_data):
        password = validated_data.pop('password', None)
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        if password:
            instance.set_password(password)
        instance.save()
        return instance

def validation_of_password(data):
    if len(data) < 6:
            raise serializers.ValidationError("Password must be at least 6 characters long.")
        
        # Check if the password contains at least one uppercase letter
    if not re.search(r'[A-Z]', data):
            raise serializers.ValidationError("Password must contain at least one uppercase letter.")
    if not re.search(r'[0-9]', data):
        raise serializers.ValidationError("Password must contain at least one digit.")
    
    return data
class CustomFieldSerializer(serializers.ModelSerializer):
    class Meta:
         model = CustomField
         fields = ['id','field_name','field_type']

class CustomFieldValueSerializerNew(serializers.ModelSerializer):
    class Meta:
        model = CustomFieldValue
        fields = ['id','custom_field', 'value']


class EmployeeProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = EmployeeProfile
        fields = ['id','position']







class EmployeeProfileSerializer(serializers.ModelSerializer):
    employeeprofile = EmployeeProfileSerializer(required=False)
    custom_fields = CustomFieldValueSerializerNew(many=True, required=False)

    class Meta:
        model = CustomUser
        fields = ['id', 'name', 'email', 'employeeprofile','custom_fields']


    def to_representation(self, instance):
        representation = super().to_representation(instance)
        custom_field_values = CustomFieldValue.objects.filter(user=instance)
        representation['custom_fields'] = [
            {   'custom_field_id':field.custom_field.id,
                'field_name': field.custom_field.field_name,
                'field_type': field.custom_field.field_type,
                'value': field.value or "",  # Show empty string if no value
            }
            for field in custom_field_values
        ]
        position_id=representation['employeeprofile']['position']
       
        try:
            position = Position.objects.get(id=position_id)
            representation['employeeprofile']['position_title'] = position.title
        except Position.DoesNotExist:
            representation['employeeprofile']['position_title'] = None
    
        return representation

    def validate(self, data):
        profile_data = data.get('employeeprofile', {})
        if 'position' in profile_data and profile_data['position'] is None:
            raise serializers.ValidationError("Position must be provided.")
        return data

    def update(self, instance, validated_data):
        profile_data = validated_data.pop('employeeprofile', {})
        custom_fields_data = validated_data.pop('custom_fields', [])
        
        # Update the user instance
        instance = super().update(instance, validated_data)
        
        # Update or create the employee profile
        employee_profile, created = EmployeeProfile.objects.get_or_create(user=instance)

        if profile_data:
            if 'position' in profile_data:
                employee_profile.position = profile_data['position']
            if 'profile_image' in profile_data:
                employee_profile.profile_image = profile_data['profile_image']
            employee_profile.save()

        # Process custom fields
        for custom_field_data in custom_fields_data:
            custom_field_instance = custom_field_data.get('custom_field')
            field_name = custom_field_instance.field_name if custom_field_instance else None
            value = custom_field_data.get('value')

            if value is None:
                print(f"Skipping update for custom field due to missing value: {custom_field_data}")
                continue

            if not field_name:
                print(f"Skipping update for custom field due to missing field_name: {custom_field_data}")
                continue

            print(f"Processing custom field: {field_name}, Value: {value}")

            try:
                custom_field = CustomField.objects.get(field_name=field_name)
                custom_field_value, created = CustomFieldValue.objects.get_or_create(
                    user=instance,
                    custom_field=custom_field
                )
                custom_field_value.value = value
                custom_field_value.save()
                print(f"{'Created' if created else 'Updated'} Custom Field: {field_name}, Value: {value}")

            except CustomField.DoesNotExist:
                print(f"CustomField '{field_name}' does not exist. Skipping...")

        instance.employeeprofile = employee_profile
        return instance


# change password 

class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)

    def validate_old_password(self, value):
        user = self.context['request'].user
        if not user.check_password(value):
            raise serializers.ValidationError("Old password is incorrect.")
        return value

    def validate_password(self, value):
        return validation_of_password(value)
    


class EmployeeviewPositionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Position
        fields = ['id', 'title']





class EmployeeProfilePicSerializer(serializers.ModelSerializer):
    class Meta:
        model = EmployeeProfile
        fields = ['profile_image']
