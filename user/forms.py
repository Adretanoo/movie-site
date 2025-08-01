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
    card_number = forms.CharField(validators=[card_validator],widget=forms.TextInput(attrs={
    }))
    phone = forms.CharField(validators=[phone_validator],
                            widget=forms.TextInput(attrs={
                                'placeholder':'+380 00 000 0000'
    }))
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'email', 'phone', 'address', 'card_number',
                  'language', 'gender', 'birthday', 'city']
