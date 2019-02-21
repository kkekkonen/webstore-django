from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from webstore_django.models import Product
from django.forms import ModelForm

class SignupForm(UserCreationForm):
    email = forms.EmailField(label='Email', required=True)
    first_name = forms.CharField(label='First name', max_length=30, required=True)
    last_name = forms.CharField(label='Last name', max_length=30, required=True)

    class Meta:
        model = User
        fields = (
            'username',
            'first_name',
            'last_name',
            'email',
            'password1',
            'password2',
        )

    def __init__(self, *args, **kwargs):
        super(SignupForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'
        if self.errors:
            for f_name in self.fields:
                if f_name in self.errors:
                    self.fields[f_name].widget.attrs['class'] = "form-control error"

    def save(self, commit=True):
        user = super(SignupForm, self).save(commit=False)
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']

        if commit:
            user.save()
        return user

class ProductForm(ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'code', 'description', 'cost']
    def __init__(self, *args, **kwargs):
        super(ProductForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'
        if self.errors:
            for f_name in self.fields:
                if f_name in self.errors:
                    self.fields[f_name].widget.attrs['class'] = "form-control error"
