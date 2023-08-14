from django import forms
from .models import CustomUser
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm

class registerUser(UserCreationForm):
    password1 = forms.CharField(
        label="Password",
        widget=forms.PasswordInput(attrs={'class':'style2-input ps-5 form-control text-grey-900 font-xsss fw-600', 'type':'password', 'align':'center', 'placeholder':'Create Password'}),
    )
    password2 = forms.CharField(
        label="Confirm password",
        widget=forms.PasswordInput(attrs={'class':'style2-input ps-5 form-control text-grey-900 font-xsss fw-600', 'type':'password', 'align':'center', 'placeholder':'Confirm Password'}),
    )

    class Meta:
        model = CustomUser  #database 
        fields = ('username','first_name','email','password1', 'password2','gender','b_date','p_img')
        widgets = {
                'username':forms.TextInput(attrs={'class':'style2-input ps-5 form-control text-grey-900 font-xsss fw-600','placeholder':'Enter Username'}),
                'first_name':forms.TextInput(attrs={'class':'style2-input ps-5 form-control text-grey-900 font-xsss fw-600','placeholder':'Enter Full Name'}),
                
                'email':forms.TextInput(attrs={'class':'style2-input ps-5 form-control text-grey-900 font-xsss fw-600','placeholder':'Enter Your Email'}),
                'contact':forms.TextInput(attrs={'class':'style2-input ps-5 form-control text-grey-900 font-xsss fw-600','placeholder':'Enter Your Contact'}),
                # 'password1':forms.TextInput(attrs={'class':'style2-input ps-5 form-control text-grey-900 font-xsss fw-600','type':'password','style':'width:350px'}),
                'password2':forms.TextInput(attrs={'class':'style2-input ps-5 form-control text-grey-900 font-xsss fw-600'}),
                'b_date':forms.NumberInput(attrs={'class': 'style2-input ps-5 form-control text-grey-900 font-xsss fw-600','type':'date'}),
                'age': forms.TextInput(attrs={'class':'style2-input ps-5 form-control text-grey-900 font-xsss fw-600','placeholder':'Enter Age'}),
                # 'gender':forms.CheckboxInput(attrs={'class':"form-group",'type':'checkbox','style':'height:10px'}),
                'gender':forms.RadioSelect(attrs={'class':"",'type':'radio'})
        }
    
class loginUser(AuthenticationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control','placeholder': 'Username'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control','placeholder':'Password'}))
        
