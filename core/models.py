

import uuid
from django.db import models
from django.conf import settings
from django.utils import timezone
from django.contrib.auth import User,


class UserProfile(models.Model):
    

    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,   # Delete profile when user is deleted
        related_name='profile'
    )

    
    is_email_verified = models.BooleanField(
        default=False,
        help_text='True once the user clicks the verification link in their email.'
    )

    avatar = models.ImageField(
        upload_to='avatars/',
        null=True,
        blank=True
    )

    bio = models.TextField(blank=True, max_length=300)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'Profile of {self.user.username}'


class EmailVerificationToken(models.Model):
    

    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='email_verification_token'
    )

    
    token = models.UUIDField(default=uuid.uuid4, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def is_expired(self):
       
        timeout = getattr(settings, 'EMAIL_VERIFICATION_TIMEOUT', 86400)
        return (timezone.now() - self.created_at).total_seconds() > timeout

    def __str__(self):
        return f'Verification token for {self.user.email}'

# Keep a backwards-compatible alias matching existing migrations
# which used the name 'Userprofile' (lowercase 'p').
Userprofile = UserProfile
