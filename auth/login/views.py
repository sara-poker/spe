from django.shortcuts import redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth import get_user_model
from django.contrib import messages
from auth.views import AuthView
from django.urls import reverse

User = get_user_model()


class LoginView(AuthView):
    def get(self, request):
        if request.user.is_authenticated:
            return redirect("index")
        return super().get(request)

    def post(self, request):
        if request.method == "POST":
            username = request.POST.get("email-username")
            password = request.POST.get("password")

            if not (username and password):
                messages.error(request, "لطفا نام کاربری و رمز ورود را وارد کنید.")
                return redirect("login")

            # اگر ایمیل وارد شده
            if "@" in username:
                user_email = User.objects.filter(email=username).first()
                if user_email is None:
                    messages.error(request, "ایمیلی معتبر وارد کنید.")
                    return redirect("login")
                username = user_email.username

            user = User.objects.filter(username=username).first()
            if user is None:
                messages.error(request, "نام کاربری معتبر وارد کنید.")
                return redirect("login")

            authenticated_user = authenticate(request, username=username, password=password)
            if authenticated_user is not None:
                login(request, authenticated_user)
                next_url = request.POST.get("next") or request.GET.get("next") or reverse("index")
                return redirect(next_url)
            else:
                messages.error(request, "نام کاربری یا رمز ورود اشتباه است.")
                return redirect("login")
