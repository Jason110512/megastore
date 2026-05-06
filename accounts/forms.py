from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import Usuario


class LoginForm(AuthenticationForm):
    username = forms.CharField(
        label='Usuario',
        widget=forms.TextInput(attrs={'placeholder': 'Usuario', 'class': 'form-control'})
    )
    password = forms.CharField(
        label='Contraseña',
        widget=forms.PasswordInput(attrs={'placeholder': 'Contraseña', 'class': 'form-control'})
    )


class RegistroForm(UserCreationForm):
    nombre_completo = forms.CharField(
        max_length=150,
        widget=forms.TextInput(attrs={'placeholder': 'Nombre Completo', 'class': 'form-control'})
    )
    correo = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs={'placeholder': 'Correo Electrónico', 'class': 'form-control'})
    )
    username = forms.CharField(
        widget=forms.TextInput(attrs={'placeholder': 'Usuario', 'class': 'form-control'})
    )
    password1 = forms.CharField(
        label='Contraseña',
        widget=forms.PasswordInput(attrs={'placeholder': 'Contraseña', 'class': 'form-control'})
    )
    password2 = forms.CharField(
        label='Confirmar Contraseña',
        widget=forms.PasswordInput(attrs={'placeholder': 'Confirmar Contraseña', 'class': 'form-control'})
    )

    class Meta:
        model = Usuario
        fields = ['nombre_completo', 'username', 'password1', 'password2', 'correo']

    def save(self, commit=True):
        user = super().save(commit=False)
        user.nombre_completo = self.cleaned_data['nombre_completo']
        user.correo = self.cleaned_data['correo']
        user.email = self.cleaned_data['correo']
        user.rol = 'cliente'
        if commit:
            user.save()
        return user


class UsuarioAdminForm(forms.ModelForm):
    class Meta:
        model = Usuario
        fields = ['nombre_completo', 'username', 'correo', 'rol', 'activo']
        widgets = {
            'nombre_completo': forms.TextInput(attrs={'class': 'form-control'}),
            'username': forms.TextInput(attrs={'class': 'form-control'}),
            'correo': forms.EmailInput(attrs={'class': 'form-control'}),
            'rol': forms.Select(attrs={'class': 'form-select'}),
            'activo': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }
