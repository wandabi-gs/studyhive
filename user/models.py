from django.contrib.auth.models import (
    AbstractBaseUser, BaseUserManager, PermissionsMixin
)
from django.db import models
from uuid import uuid4


class CustomUserManager(BaseUserManager):
    def create_superuser(self, email, password=None):
        email = self.normalize_email(email)
        user = self.model(email=email)
        user.set_password(password)
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user


class CustomUser(AbstractBaseUser, PermissionsMixin):
    uid = models.CharField(max_length=50, default=uuid4, unique=True)
    email = models.EmailField(unique=True)
    image = models.ImageField(upload_to="profiles/", null=True, blank=True)
    username = models.CharField(max_length=50, blank=True)
    password_reset = models.BooleanField(default=False)
    image = models.ImageField(upload_to="profiles/", default='profiles/default.webp')
    private = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.email


class Connection(models.Model):
    uid = models.CharField(max_length=50, default=uuid4, unique=True)
    user = models.ForeignKey(
        to=CustomUser, to_field="uid",
        related_name="user",
        on_delete=models.CASCADE)
    connection = models.ForeignKey(
        to=CustomUser,
        to_field="uid",
        related_name="connection",
        null=True,
        on_delete=models.SET_NULL)
    connection_status = models.CharField(
        max_length=10,
        choices=(('pending', 'pending'), ('accepted',
                 'accepted'), ('revoked', 'revoked')))
    created_at = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return f"{self.user.email} - {self.connection.email}"


class ReportedUser(models.Model):
    uid = models.CharField(max_length=50, default=uuid4, unique=True)
    user = models.ForeignKey(
        to=CustomUser, to_field="uid",
        related_name="reported_user",
        on_delete=models.CASCADE)
    reporter = models.ForeignKey(
        to=CustomUser, to_field="uid",
        related_name="reporter",
        null=True, on_delete=models.SET_NULL)
    reason = models.TextField(blank=True, null=True)
    banned = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)