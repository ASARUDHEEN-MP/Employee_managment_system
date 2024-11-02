from django.db import models

class Position(models.Model):
    title = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.title

class CustomField(models.Model):
    FIELD_TYPES = [
        ('text', 'Text'),
        ('number', 'Number'),
        ('date', 'Date'),
        ('boolean', 'Boolean'),
    ]
    
    field_name = models.CharField(max_length=100)
    field_type = models.CharField(max_length=50, choices=FIELD_TYPES)

    def __str__(self):
        return self.field_name