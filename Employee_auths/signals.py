from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import CustomUser, EmployeeProfile

@receiver(post_save, sender=CustomUser)
def create_employee_profile(sender, instance, created, **kwargs):
    if created and not instance.is_superuser:
        EmployeeProfile.objects.create(user=instance)

@receiver(post_save, sender=CustomUser)
def save_employee_profile(sender, instance, **kwargs):
    if not instance.is_superuser and hasattr(instance, 'employeeprofile'):
        instance.employeeprofile.save()
