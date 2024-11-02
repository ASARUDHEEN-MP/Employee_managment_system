from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import AdminOnlyView,PositionViewSet,Custom_fields,Custom_fields_value,FieldTypesView
# Adjust the import based on your project structure

# Create a router and register the AdminOnlyView
router = DefaultRouter()
router.register(r'Employees', AdminOnlyView, basename='admin-Employees')
router.register(r'positions', PositionViewSet)
router.register(r'custom_fields', Custom_fields)
router.register(r'custom_fields_value', Custom_fields_value)


urlpatterns = [
    path('', include(router.urls)),  # Include the router's URLs
    path('field_types/', FieldTypesView.as_view(), name='field-types'),
]
