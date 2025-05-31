from django.shortcuts import redirect
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from django.contrib import messages
from django.conf import settings
from auth.views import AuthView
from auth.helpers import send_verification_email
from auth.models import Profile
import uuid

User = get_user_model()

class RegisterView(AuthView):
    def get(self, request):
        if request.user.is_authenticated:
            return redirect("index")
        return super().get(request)

    def post(self, request):
        username = request.POST.get("username")
        email = request.POST.get("email")
        password = request.POST.get("password")

        # Check if username or email already exist separately
        if User.objects.filter(username=username).exists():
            messages.error(request, "این نام کاربری قبلا در سیستم ثبت شده است.")
            return redirect("register")

        if User.objects.filter(email=email).exists():
            messages.error(request, "این ایمیل قبلا در سیستم ثبت شده است.")
            return redirect("register")

        # Create the user and set their password
        created_user = User.objects.create_user(username=username, email=email, password=password)

        # Add the user to the 'client' group
        user_group, created = Group.objects.get_or_create(name="client")
        created_user.groups.add(user_group)

        # Generate a token and send a verification email here
        token = str(uuid.uuid4())

        # Set the token in the user's profile
        user_profile, created = Profile.objects.get_or_create(user=created_user)
        user_profile.email_token = token
        user_profile.email = email
        user_profile.save()

        send_verification_email(email, token)

        if settings.EMAIL_HOST_USER and settings.EMAIL_HOST_PASSWORD:
            messages.success(request, "ایمیل تایید با موفقیت ارسال شد")
        else:
            messages.error(request, "تنظیمات ایمیل به درستی تنظیم نشده است و امکان ارسال ایمیل وجود ندارد.")

        request.session['email'] = email
        return redirect("verify-email-page")
