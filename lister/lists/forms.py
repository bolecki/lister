from django import forms

class CreateListForm(forms.Form):
    name = forms.CharField(label='Name', max_length=100)
    public = forms.BooleanField(required=False)

    def __init__(self, *args, **kwargs):
        show_public = kwargs.pop('authenticated', False)

        super(CreateListForm, self).__init__(*args, **kwargs)
        if not show_public:
            self.fields['public'].widget = forms.HiddenInput()
            self.fields['public'].initial = True

class LoginForm(forms.Form):
    user = forms.CharField(label="Username", max_length=30)
    password = forms.CharField(label="Password", widget=forms.PasswordInput())
