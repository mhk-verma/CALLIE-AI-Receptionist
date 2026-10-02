from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models
from django.utils.translation import gettext_lazy as _
import uuid


class UserManager(BaseUserManager):
    """Custom user manager for email-based authentication."""
    
    def create_user(self, email, password=None, **extra_fields):
        """Create and save a regular user with the given email and password."""
        if not email:
            raise ValueError(_('The Email field must be set'))
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        """Create and save a superuser with the given email and password."""
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError(_('Superuser must have is_staff=True.'))
        if extra_fields.get('is_superuser') is not True:
            raise ValueError(_('Superuser must have is_superuser=True.'))

        return self.create_user(email, password, **extra_fields)


class User(AbstractUser):
    """Custom User model with email as the primary identifier."""
    
    class Role(models.TextChoices):
        OWNER = 'owner', _('Owner')
        STAFF = 'staff', _('Staff')
        ADMIN = 'admin', _('Admin')

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    email = models.EmailField(_('email address'), unique=True)
    username = None  # Remove username field
    role = models.CharField(
        max_length=20,
        choices=Role.choices,
        default=Role.OWNER,
        verbose_name=_('Role')
    )
    phone = models.CharField(max_length=20, blank=True, null=True, verbose_name=_('Phone'))
    avatar = models.ImageField(upload_to='avatars/', blank=True, null=True, verbose_name=_('Avatar'))
    email_verified = models.BooleanField(default=False, verbose_name=_('Email Verified'))
    onboarding_completed = models.BooleanField(default=False, verbose_name=_('Onboarding Completed'))
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_('Created At'))
    updated_at = models.DateTimeField(auto_now=True, verbose_name=_('Updated At'))

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']

    objects = UserManager()

    class Meta:
        verbose_name = _('User')
        verbose_name_plural = _('Users')
        ordering = ['-created_at']

    def __str__(self):
        return self.email

    def get_full_name(self):
        """Return the full name of the user."""
        return f"{self.first_name} {self.last_name}".strip()

    def is_owner(self):
        """Check if user is an owner."""
        return self.role == self.Role.OWNER

    def is_staff_member(self):
        """Check if user is a staff member."""
        return self.role == self.Role.STAFF

    def is_admin_user(self):
        """Check if user is an admin."""
        return self.role == self.Role.ADMIN


class PasswordReset(models.Model):
    """Model for password reset tokens."""
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='password_resets')
    token = models.CharField(max_length=255, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField()
    used = models.BooleanField(default=False)

    class Meta:
        verbose_name = _('Password Reset')
        verbose_name_plural = _('Password Resets')
        ordering = ['-created_at']

    def __str__(self):
        return f"Password reset for {self.user.email}"

    def is_valid(self):
        """Check if the token is still valid."""
        from django.utils import timezone
        return not self.used and self.expires_at > timezone.now()


class EmailVerification(models.Model):
    """Model for email verification tokens."""
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='email_verifications')
    token = models.CharField(max_length=255, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField()
    used = models.BooleanField(default=False)

    class Meta:
        verbose_name = _('Email Verification')
        verbose_name_plural = _('Email Verifications')
        ordering = ['-created_at']

    def __str__(self):
        return f"Email verification for {self.user.email}"

    def is_valid(self):
        """Check if the token is still valid."""
        from django.utils import timezone
        return not self.used and self.expires_at > timezone.now()
