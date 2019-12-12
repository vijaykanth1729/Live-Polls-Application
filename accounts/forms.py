from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
#from captcha.fields import CaptchaField



class UserRegistrationForm(forms.Form):
    username = forms.CharField(label='UserName', max_length=100,
                               widget=forms.TextInput(attrs={'class':'form-control'}))
    email = forms.EmailField(label='Email:', widget=forms.TextInput(attrs={'class':'form-control'}))
    password1 = forms.CharField(label='Password',
                                max_length=20,
                                min_length=5,
                                widget=forms.PasswordInput(attrs={'class':'form-control'}))

    password2 = forms.CharField(label='Confirm Password',
                                max_length=20,
                                min_length=5,
                                widget=forms.PasswordInput(attrs={'class':'form-control'}))
    #captcha = CaptchaField()

    def clean_username(self):
        username = self.cleaned_data['username']
        qs = User.objects.filter(username=username)
        if qs.exists():
            raise ValidationError('Choose Different Username!!')
        return username

    def clean_email(self):
        ''' populates the error exactly right above the field... '''

        email = self.cleaned_data['email']
        qs = User.objects.filter(email=email)
        if qs.exists():
            raise ValidationError('Email Already Exists Choose Different One')
        return email
    # def clean_password2(self):
    #     p1 = self.cleaned_data['password1']
    #     p2 = self.cleaned_data['password2']
    #     if p1 != p2:
    #         raise ValidationError("Passwords Should Match!!")
    #     return p1

    def clean(self):
        ''' if we use clean method it populates the errors at top of the all fields.. '''

        cleaned_data = super().clean()
        p1 = cleaned_data.get('password1')
        p2 = cleaned_data.get('password2')
        # email = cleaned_data.get('email')
        # qs = User.objects.filter(email=email)
        # if qs.exists():
        #     raise ValidationError('Email Already Exists Choose Different One')

        if p1 and p2:
            if p1!=p2:
                raise ValidationError("Passwords Should Match!!!")
