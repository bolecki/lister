from django import forms

class CreateListForm(forms.Form):
    name = forms.CharField(label="", max_length=30, widget=forms.TextInput(attrs={'placeholder': 'Name'}))
    public = forms.BooleanField(required=False)

    def __init__(self, *args, **kwargs):
        show_public = kwargs.pop('authenticated', False)

        super(CreateListForm, self).__init__(*args, **kwargs)
        if not show_public:
            self.fields['public'].widget = forms.HiddenInput()
            self.fields['public'].initial = True

class LoginForm(forms.Form):
    user = forms.CharField(label="", max_length=30, widget=forms.TextInput(attrs={'placeholder': 'Username'}))
    password = forms.CharField(label="", widget=forms.PasswordInput(attrs={'placeholder': 'Password'}))
