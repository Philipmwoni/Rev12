

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import (
    authenticate, login, logout, update_session_auth_hash
)
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages
from django.utils import timezone
from django.conf import settings
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.contrib.auth.tokens import default_token_generator

from .models import UserProfile, EmailVerificationToken
from .forms import (
    RegisterForm, EmailLoginForm,
    ProfileUpdateForm, UserProfileForm, CustomPasswordChangeForm
)
from django.urls import reverse
def home(request):
    return redirect('auth:home')

def register(request):
   
    if request.user.is_authenticated:
        return redirect('auth:home')

    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            
            user = form.save(commit=False)
            user.email = form.cleaned_data['email']
            user.is_active = True  # Active but email not yet verified
            user.save()

            
            UserProfile.objects.create(user=user)

            token_obj = EmailVerificationToken.objects.create(user=user)

            verification_url = request.build_absolute_uri(
                reverse('core:verify_email', args=[token_obj.token])
            )

            send_verification_email(user, verification_url)

            messages.success(
                request,
                'Account created! Please check your email to verify your address.'
            )
            return redirect('core:login')
    else:
        form = RegisterForm()

    return render(request, 'core/register.html', {'form': form})


def send_verification_email(user, verification_url):
    
    subject = 'Verify your Expense Tracker email'
    html_message = render_to_string('emails/verification_email.html', {
        'user': user,
        'verification_url': verification_url,
    })
    plain_message = (
        f'Hi {user.username},\n\n'
        f'Please verify your email by visiting:\n{verification_url}\n\n'
        f'This link expires in 24 hours.\n\nThanks,\nExpense Tracker Team'
    )
    send_mail(
        subject=subject,
        message=plain_message,
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=[user.email],
        html_message=html_message,
        fail_silently=False,
    )


def verify_email(request, token):
    
    try:
        token_obj = EmailVerificationToken.objects.get(token=token)
    except EmailVerificationToken.DoesNotExist:
        messages.error(request, 'This verification link is invalid.')
        return redirect('core:login')

    if token_obj.is_expired():
        token_obj.delete()
        messages.error(
            request,
            'This verification link has expired. Please register again.'
        )
        return redirect('core:register')

    
    profile = token_obj.user.profile
    profile.is_email_verified = True
    profile.save()

    
    token_obj.delete()

    messages.success(request, 'Email verified! You can now log in.')
    return redirect('core:login')


def login_view(request):
    
    if request.user.is_authenticated:
        return redirect('auth:home')

    if request.method == 'POST':
        form = EmailLoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']

            # Look up the username from email
            try:
                user_obj = User.objects.get(email__iexact=email)
            except User.DoesNotExist:
                messages.error(request, 'No account found with that email.')
                return render(request, 'core/login.html', {'form': form})

            
            user = authenticate(request, username=user_obj.username, password=password)
            if user is None:
                messages.error(request, 'Incorrect password. Please try again.')
                return render(request, 'core/login.html', {'form': form})

            
            if not user.profile.is_email_verified:
                messages.warning(
                    request,
                    'Please verify your email before logging in. '
                    'Check your inbox for the verification link.'
                )
                return render(request, 'core/login.html', {'form': form})

            login(request, user)
            
            next_url = request.GET.get('next', 'auth:home')
            return redirect(next_url)
    else:
        form = EmailLoginForm()

    return render(request, 'core/login.html', {'form': form})


def logout_view(request):
    logout(request)
    messages.info(request, 'You have been logged out.')
    return redirect('core:login')


@login_required
def profile(request):
    user_form = ProfileUpdateForm(instance=request.user)
    profile_form = UserProfileForm(instance=request.user.profile)

    if request.method == 'POST':
        user_form = ProfileUpdateForm(request.POST, instance=request.user)
        profile_form = UserProfileForm(request.POST, instance=request.user.profile)

        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, 'Profile updated successfully!')
            return redirect('core:profile')

    return render(request, 'core/profile.html', {
        'user_form': user_form,
        'profile_form': profile_form,
    })


@login_required
def change_password(request):
    
    if request.method == 'POST':
        form = CustomPasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            messages.success(request, 'Password changed successfully!')
            return redirect('core:profile')
    else:
        form = CustomPasswordChangeForm(request.user)

    return render(request, 'core/change_password.html', {'form': form})


def password_reset_request(request):
    
    if request.method == 'POST':
        email = request.POST.get('email', '').strip()

        try:
            user = User.objects.get(email__iexact=email)
            token = default_token_generator.make_token(user)
            uid = urlsafe_base64_encode(force_bytes(user.pk))

            reset_url = request.build_absolute_uri(
                reverse('core:password_reset_confirm', args=[uid, token])
            )

            subject = 'Reset your Expense Tracker password'
            subject = 'Reset your Expense Tracker password'
            html_message = render_to_string('emails/password_reset_email.html', {
                'user': user,
                'reset_url': reset_url,
            })
            send_mail(
                subject=subject,
                message=f'Reset your password: {reset_url}',
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[user.email],
                html_message=html_message,
                fail_silently=True,
            )
        except User.DoesNotExist:
            pass  # Don't reveal whether email exists

        messages.success(
            request,
            'If an account exists with that email, you will receive a reset link shortly.'
        )
        return redirect('core:login')

    return render(request, 'core/password_reset_request.html')


def password_reset_confirm(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is None or not default_token_generator.check_token(user, token):
        messages.error(request, 'This password reset link is invalid or has expired.')
        return redirect('core:password_reset_request')

    if request.method == 'POST':
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')

        if password1 != password2:
            messages.error(request, 'Passwords do not match.')
        elif len(password1) < 8:
            messages.error(request, 'Password must be at least 8 characters.')
        else:
            user.set_password(password1)
            user.save()
            messages.success(request, 'Password reset! You can now log in.')
            return redirect('core:login')

    return render(request, 'core/password_reset_confirm.html', {
        'uidb64': uidb64,
        'token': token,
    })
