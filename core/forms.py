from django import forms
from django.contrib.auth.models import User

from .models import Profile


class CreateUserForm(forms.Form):
    first_name = forms.CharField(max_length=100)
    last_name = forms.CharField(max_length=100)

    # username is converted to email in this form
    username = forms.CharField(label='Email', help_text='@groupdesignace.com', max_length=20)

    password1 = forms.CharField(label='Password', widget=forms.PasswordInput())
    password2 = forms.CharField(label='Confirm Password', widget=forms.PasswordInput())

    def clean_username(self):
        username = self.cleaned_data.get('username')

        if username:
            if User.objects.filter(username=username).exists():
                raise forms.ValidationError('This email address is unavailable!')
            elif '@' in username or '.' in username:
                raise forms.ValidationError('Only provide the first part of the email without using @ or .')

        return username

    def clean_password2(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')
        if password1 and password2:
            if password1 != password2:
                raise forms.ValidationError(("The two password fields didn't match."))
            elif password1 == '' or password2 == '':
                raise forms.ValidationError(("The password cannot be blank"))
        return password2


class BaseProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['company', 'proximity_id', 'joining_date', 'designation', 'photo', 'gender', 'blood_group', 'religion', 'nationality']