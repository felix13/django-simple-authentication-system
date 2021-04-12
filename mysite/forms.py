from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, PasswordChangeForm


class LoginForm(forms.Form):

    username = forms.CharField(
                         max_length=30, 
                         widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Username'}))  
    
    password = forms.CharField(
                         max_length=30, 
                         widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Password'})) 


class UserRegistrationForm(UserCreationForm):
    username = forms.CharField(max_length=30, widget=forms.TextInput(attrs={'class': 'form-control'}))  
    first_name = forms.CharField(max_length=30, widget=forms.TextInput(attrs={'class': 'form-control'}))
    last_name = forms.CharField(max_length=30, widget=forms.TextInput(attrs={'class': 'form-control'}))
    email = forms.CharField(max_length=75, widget=forms.EmailInput(attrs={'class': 'form-control'}))
    password1 = forms.CharField( label="password",  max_length=100, widget=forms.PasswordInput(attrs={'class':'form-control', 'placeholder':'password'}))
    password2 = forms.CharField(label ="confirm password", max_length=100,widget=forms.PasswordInput(attrs={'class':'form-control', 'placeholder':'Confirm password'}))
                            
    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name',  'email', 'password1', 'password2')  
         
    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("Email  is already in use.")
        return email
        
      
class UserProfileForm(forms.ModelForm):
    first_name = forms.CharField(max_length=30, widget=forms.TextInput(attrs={'class': 'form-control'}), required=False)
    last_name = forms.CharField(max_length=30, widget=forms.TextInput(attrs={'class': 'form-control'}), required=False)
    email = forms.CharField(max_length=75, widget=forms.EmailInput(attrs={'class': 'form-control'}), required=False)
    
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email',)
        
         
class ChangePasswordForm(PasswordChangeForm):
    old_password = forms.CharField(widget=forms.PasswordInput(attrs={'class':'form-control', 'placeholder':'Old password'})  )
    new_password1 = forms.CharField(widget=forms.PasswordInput(attrs={'class':'form-control', 'placeholder':'New password' }) )
    new_password2 = forms.CharField(widget=forms.PasswordInput(attrs={'class':'form-control', 'placeholder':'New password confirmation' }) )
                                   
    class Meta:
        model = User
        fields = ('old_password', 'new_password1', 'new_password2',)
               
