from django.shortcuts import render ,redirect
from allauth.account import views

# Create your views here.

class LoginView(views.LoginView):
    # ログイン画面のテンプレートファイルを指定
    template_name = 'accounts/login.html'

class LogoutView(views.LogoutView):
    template_name = 'accounts/logout.html'

    def post(self, *args, **kwargs):
        if self.request.user.is_authenticated:
            self.logout()
        return redirect('/')
    
class SignupView(views.SignupView):
    template_name = 'accounts/signup.html'
    