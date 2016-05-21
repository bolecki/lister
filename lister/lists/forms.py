from django import forms
from django.core import exceptions
from django.utils.translation import ugettext_lazy as _

def validate_username(username):
    if ',' in username:
        raise exceptions.ValidationError(_('No comma in username'))

class CreateListForm(forms.Form):
    name = forms.CharField(max_length=30, widget=forms.TextInput(attrs={'placeholder': 'Name', 'class': 'form-control'}))
    public = forms.BooleanField(required=False, widget=forms.CheckboxInput(attrs={'class': 'checkbox'}))
    sortable = forms.BooleanField(required=False, widget=forms.CheckboxInput(attrs={'class': 'checkbox'}))

    def __init__(self, *args, **kwargs):
        authenticated = kwargs.pop('authenticated', False)

        super(CreateListForm, self).__init__(*args, **kwargs)
        if not authenticated:
            self.fields['public'].widget = forms.HiddenInput()
            self.fields['public'].initial = True
            self.fields['sortable'].widget = forms.HiddenInput()
            self.fields['sortable'].initial = False


class LoginForm(forms.Form):
    user = forms.CharField(label="", max_length=30, validators=[validate_username], widget=forms.TextInput(attrs={'placeholder': 'Username', 'class': 'form-control'}))
    password = forms.CharField(label="", widget=forms.PasswordInput(attrs={'placeholder': 'Password', 'class': 'form-control'}))

    def __init__(self, *args, **kwargs):
        login_attempt = kwargs.pop('login_attempt', None)

        super(LoginForm, self).__init__(*args, **kwargs)
        if login_attempt:
            self.fields['user'].widget.attrs['value'] = login_attempt


class GrantForm(forms.Form):
    users = forms.CharField(label="", max_length=100, widget=forms.TextInput(attrs={'placeholder': 'John,Jane,Frank', 'class': 'form-control'}))
