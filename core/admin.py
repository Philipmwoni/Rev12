from django.contrib import admin
from .models import UserProfile, EmailVerificationToken


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'is_email_verified', 'created_at')
    list_filter = ('is_email_verified',)
    search_fields = ('user__username', 'user__email')


@admin.register(EmailVerificationToken)
class EmailVerificationTokenAdmin(admin.ModelAdmin):
    list_display = ('user', 'token', 'created_at')
    search_fields = ('user__email',)
