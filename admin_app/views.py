from django.shortcuts import render
from rest_framework import viewsets,status
from .serializers import EmployeeSerializer,PositionSerializer,CustomFieldSerializer,CustomFieldValueSerializer
from Permission import IsAdmin
from .models import Position,CustomField
from rest_framework.response import Response
from Employee_auths.models import CustomUser,CustomFieldValue
from rest_framework.views import APIView
    

# Create your views here.

class AdminOnlyView(viewsets.ModelViewSet):
    queryset = CustomUser.objects.all()
    serializer_class = EmployeeSerializer
    permission_classes = [IsAdmin]

    def get_queryset(self):
        # Admins can view all users
        return CustomUser.objects.filter(is_superuser=False)
    
    
            
    # def list(self, request, *args, **kwargs):
    #     queryset = self.get_queryset()
    #     serializer = self.get_serializer(queryset, many=True)
    #     return Response(serializer.data)
    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()

        # Get search and filter parameters
        search = request.query_params.get('search', None)
        position = request.query_params.get('position', None)

        # Apply search filter
        if search:
            queryset = queryset.filter(name__icontains=search)

        # Apply position filter if specified
        if position:
            queryset = queryset.filter(employeeprofile__position__name=position)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
    


class PositionViewSet(viewsets.ModelViewSet):
    queryset = Position.objects.all()
    serializer_class = PositionSerializer
    permission_classes = [IsAdmin]


class Custom_fields(viewsets.ModelViewSet):
    queryset=CustomField.objects.all()
    serializer_class=CustomFieldSerializer
    permission_classes=[IsAdmin]

class FieldTypesView(APIView):
    def get(self, request):
        field_types = CustomField.FIELD_TYPES
        return Response(field_types)
    

    
class Custom_fields_value(viewsets.ModelViewSet):
    queryset = CustomFieldValue.objects.all()
    serializer_class = CustomFieldValueSerializer
    permission_classes = [IsAdmin]

    def create(self, request, *args, **kwargs):
        # Use custom_field_id from the request data
        custom_field_id = request.data.get('custom_field_id')
        if custom_field_id:
            request.data['custom_field'] = custom_field_id  # Set custom_field to ID for creation

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def get_queryset(self):
        user_id = self.request.query_params.get('user_id')
        if user_id:
            return CustomFieldValue.objects.filter(user_id=user_id)
        return CustomFieldValue.objects.all()


