from django.contrib.auth.models import AbstractUser
from django.db import models

# Create your models here.

class User(AbstractUser):
    ROLE_CHOICES = [
        ('admin', 'Administrator'),
        ('jury', 'Jury'),
        ('team', 'Team'),
    ]

    role = models.CharField(max_length=10, choices=ROLE_CHOICES)
    display_name = models.CharField(max_length=100, blank=True, null=True)
    affiliation = models.CharField(max_length=100, blank=True, null=True)
    team_name = models.CharField(max_length=100, blank=True, null=True)
    is_active = models.BooleanField(default=True)

    def is_admin(self):
        return self.role == 'admin'

    def is_jury(self):
        return self.role == 'jury'

    def is_team(self):
        return self.role == 'team'

    def __str__(self):
        return f"{self.team_name} ({self.get_role_display()})"