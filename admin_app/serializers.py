from rest_framework import serializers, validators
from Employee_auths.models import CustomUser,EmployeeProfile
from .models import Position,CustomField
from Employee_auths.models import CustomFieldValue





class PositionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Position
        fields = ['id', 'title']




class CustomFieldSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomField
        fields = ['id', 'field_name', 'field_type']

   

class EmployeeProfileSerializer(serializers.ModelSerializer):
    position = PositionSerializer()  # Include position in the profile serializer

    class Meta:
        model = EmployeeProfile
        fields = ['user', 'profile_image', 'position'] 
    
class EmployeeSerializer(serializers.ModelSerializer):
    profile = EmployeeProfileSerializer(source='employeeprofile', required=False)
    class Meta:
        model = CustomUser
        fields = ['id', 'name', 'email','is_active','profile']



# class CustomFieldValueSerializer(serializers.ModelSerializer):
#     custom_field = CustomFieldSerializer(read_only=True)  # This should give you the detailed custom field

#     class Meta:
#         model = CustomFieldValue
#         fields = ['id', 'user', 'custom_field', 'value']  # Include custom_field to get its details

#     extra_kwargs = {
#         'value': {'required': False}  # Make value optional
#     }

# class CustomFieldValueSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = CustomFieldValue
#         fields = ['id', 'user', 'custom_field', 'value']

#     extra_kwargs = {
#         'value': {'required': False},
#         'custom_field': {'required': True}  # Make sure custom_field is required
#     }

class CustomFieldValueSerializer(serializers.ModelSerializer):
    custom_field = CustomFieldSerializer(read_only=True)  # For detailed output

    # This field will allow input for creation
    custom_field_id = serializers.IntegerField(write_only=True)

    class Meta:
        model = CustomFieldValue
        fields = ['id', 'user', 'custom_field', 'custom_field_id', 'value']  # Include custom_field_id for creation

    extra_kwargs = {
        'value': {'required': False},  # Make value optional
        'user': {'required': True},  # Ensure user is required
    }

    def create(self, validated_data):
        user = validated_data['user']
        custom_field_id = validated_data['custom_field_id']

        # Check if a CustomFieldValue already exists for this user and custom_field
        if CustomFieldValue.objects.filter(user=user, custom_field_id=custom_field_id).exists():
            raise serializers.ValidationError("This user already has a value for this custom field.")

        # If it doesn't exist, create the new instance
        return super().create(validated_data)
