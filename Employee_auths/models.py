from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models
from admin_app.models import Position,CustomField
from django.core.exceptions import ValidationError


class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set.')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_superuser', True)
        
        # Allow is_staff to be set to False if desired
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user(email, password, **extra_fields)

class CustomUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True)
    name = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)  # Can be False for superusers
    is_superuser = models.BooleanField(default=False)  # Superuser flag

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name']

    objects = CustomUserManager()

    def __str__(self):
        return self.email





# here no need of access by admin only view access 
class EmployeeProfile(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    profile_image = models.ImageField(upload_to='profile_images/', null=True, blank=True)
    position = models.ForeignKey(Position, on_delete=models.SET_NULL, null=True, blank=True)
   

    def __str__(self):
        return f"{self.user.name} Profile"
    
    def delete(self, *args, **kwargs):
        # Check for related custom fields before allowing deletion
        if CustomFieldValue.objects.filter(user=self.user).exists():
            raise ValidationError("Cannot delete EmployeeProfile until related CustomFieldValues are deleted.")
        super().delete(*args, **kwargs)



class CustomFieldValue(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='field_values')
    custom_field = models.ForeignKey(CustomField, on_delete=models.CASCADE, related_name='field_values')
    value = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.custom_field.field_name}: {self.value}"