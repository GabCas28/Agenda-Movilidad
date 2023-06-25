from django.contrib.auth.forms import UserCreationForm
from captcha.fields import ReCaptchaField


class AccountForm(UserCreationForm):
    captcha = ReCaptchaField()
