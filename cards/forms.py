from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from models import *


class EmailUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True)
    first_name = forms.CharField(max_length=30)
    last_name = forms.CharField(max_length=30)
    phone = models.CharField(max_length=12, help_text="Format should be: 650-111-2222")
    balance = 100
    class Meta:
        model = Player
        fields = ("first_name", "last_name", "username", "email", "phone", "password1", "password2", "balance")

    def clean_username(self):
            # Since User.username is unique, this check is redundant,
            # but it sets a nicer error message than the ORM. See #13147.
            username = self.cleaned_data["username"]
            try:
                Player.objects.get(username=username)
            except Player.DoesNotExist:
                return username
            raise forms.ValidationError(
                self.error_messages['duplicate_username'],
                code='duplicate_username',
            )


class AddBalance(forms.Form):
    add_to = forms.IntegerField(min_value=1, max_value=999)

    class Meta:
        model = Player
        fields = ('add_to')


class Bet(forms.Form):
    bet_amount = forms.IntegerField(min_value=1, max_value=999)

    class Meta:
        model = WarGame
        fields = ('bet_amount')