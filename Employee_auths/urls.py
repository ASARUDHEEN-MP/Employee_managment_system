from django.contrib import admin
from django.urls import path,include
from . import views
from rest_framework_simplejwt.views import TokenRefreshView
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'Employee',views.EmployeeView , basename='Employee_profile')


urlpatterns = [
   path('register/', views.RegisterView.as_view(), name='register'),
   path('login/', views.LoginView.as_view(), name='login'),
   path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
   path('', include(router.urls)),
   path('change-password/', views.ChangePasswordView.as_view(), name='change-password'),
   path('postion_view/', views.PostionView.as_view(), name='Postion-View'),
   path('upload-image/', views.EmployeeProfileImageUpload.as_view(), name='upload-image'),
   
]
