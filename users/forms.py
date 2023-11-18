from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django import forms

from mailsender.forms import StyleFormMixin
from users.models import User


class UserRegisterForm(StyleFormMixin, UserCreationForm):
    """
    Форма для регистрации пользователя
    """
    class Meta:
        model = User
        fields = ('email', 'password1', 'password2')


class UserProfileForm(StyleFormMixin, UserChangeForm):
    """
    Форма для редактирования профиля пользователя
    """
    class Meta:
        model = User
        fields = ('email', 'first_name', 'last_name', 'phone', 'avatar', 'country')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['password'].widget = forms.HiddenInput()


class UserResetPasswordForm(StyleFormMixin, forms.Form):
    """
    Форма для сброса пароля
    """
    username = forms.CharField(label='Имя пользователя', max_length=150)
