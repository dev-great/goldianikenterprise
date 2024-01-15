from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django.utils import timezone
from authorization.models import CustomUser

User = get_user_model()


class RegisterForm(forms.ModelForm):
    """
    The default 

    """

    password = forms.CharField(widget=forms.PasswordInput)
    password_2 = forms.CharField(
        label='Confirm Password', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['email']

    def clean_email(self):
        '''
        Verify email is available.
        '''
        email = self.cleaned_data.get('email')
        qs = User.objects.filter(email=email)
        if qs.exists():
            raise forms.ValidationError("email is taken")
        return email

    def clean(self):
        '''
        Verify both passwords match.
        '''
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        password_2 = cleaned_data.get("password_2")
        if password is not None and password != password_2:
            self.add_error("password_2", "Your passwords must match")
        return cleaned_data


class UserAdminCreationForm(UserCreationForm):
    is_Landlord = forms.BooleanField(required=False)
    is_Subscriber = forms.BooleanField(required=False)
    address = forms.CharField(max_length=100, required=False)
    phone_number = forms.CharField(max_length=30, required=False)

    class Meta:
        model = CustomUser
        fields = ['email', "password", 'first_name', 'last_name', 'is_active', 'is_staff',
                  'is_superuser', 'groups', 'user_permissions', 'last_login', 'date_joined']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['is_staff'].initial = True
        self.fields['is_superuser'].initial = False
        self.fields['groups'].initial = []
        self.fields['user_permissions'].initial = []
        self.fields['last_login'].initial = None
        self.fields['date_joined'].initial = timezone.now()

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password('password')
        if commit:
            user.save()
        return user


class UserAdminChangeForm(forms.ModelForm):

    class Meta:
        model = User
        fields = ['email', 'password', 'is_active', 'is_superuser']

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password('password')
        if commit:
            user.save()
        return user
