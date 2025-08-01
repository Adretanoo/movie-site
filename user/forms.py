from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.core.validators import RegexValidator

from adminlte.models import Language, Gender, City
from user.models import User

phone_validator = RegexValidator(
    regex=r'^\+?1?\d{9,15}$',
    message="Формат +000 00 000 0000"
)

card_validator = RegexValidator(
    regex=r'^\d{13,16}',
    message="Номер карти повинен містити від 13 до 16 цифр"
)


class UserRegisterForm(UserCreationForm):
    language = forms.ChoiceField(
        choices=Language.choices,
        widget=forms.RadioSelect,
        required=True
    )
    gender = forms.ChoiceField(
        choices=Gender.choices,
        widget=forms.RadioSelect,
        required=True
    )
    birthday = forms.DateField(widget=forms.DateInput(attrs={
        'type': 'date',
    }, format='%Y-%m-%d'))

    city = forms.ModelChoiceField(
        queryset=City.objects.all(),
        required=True,
        empty_label=None,
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    card_number = forms.CharField(validators=[card_validator], widget=forms.TextInput(attrs={
    }))
    phone = forms.CharField(validators=[phone_validator],
                            widget=forms.TextInput(attrs={
                                'placeholder': '+380 00 000 0000'
                            }))

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'email', 'phone', 'address', 'card_number',
                  'language', 'gender', 'birthday', 'city']

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_card_number(self.cleaned_data['card_number'])
        if commit:
            user.save()
        return user


class UserEditProfileForm(forms.ModelForm):
    new_card_number = forms.CharField(validators=[card_validator], label="Номер картки", required=False, max_length=16)
    new_password1 = forms.CharField(widget=forms.PasswordInput(),required=False)
    new_password2 = forms.CharField(widget=forms.PasswordInput(), required=False)
    phone = forms.CharField(validators=[phone_validator],
                            widget=forms.TextInput(attrs={
                                'placeholder': '+380 00 000 0000'
                            }))
    language = forms.ChoiceField(
        choices=Language.choices,
        widget=forms.RadioSelect,
        required=True
    )
    gender = forms.ChoiceField(
        choices=Gender.choices,
        widget=forms.RadioSelect,
        required=True
    )
    birthday = forms.DateField(widget=forms.DateInput(attrs={
        'type': 'date',
    }, format='%Y-%m-%d'))

    city = forms.ModelChoiceField(
        queryset=City.objects.all(),
        required=True,
        empty_label=None,
        widget=forms.Select(attrs={'class': 'form-control'})
    )

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'email', 'phone', 'address',
                   'language', 'gender', 'birthday', 'city','new_password1','new_password2']

    def save(self, commit=True):
        user = super().save(commit=False)
        new_card_number = self.cleaned_data.get('new_card_number')
        new_password = self.cleaned_data.get("new_password1")

        if new_password:
            user.set_password(new_password)
        if new_card_number:
            user.set_card_number(new_card_number)

        if commit:
            user.save()
        return user

    def clean(self):
        cleaned_data = super().clean()
        new_password1 = cleaned_data.get("new_password1")
        new_password2 = cleaned_data.get("new_password2")

        if new_password1 and new_password1 != new_password2:
            self.add_error('new_password2', "Паролі не співпадають.")

        return cleaned_data