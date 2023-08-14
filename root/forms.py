from django import forms
from .models import Post,Market


class createPostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['content','video','photo']
        widgets = {
            'content':  forms.Textarea(attrs={'class':'h100 bor-0 w-100 rounded-xxl p-2 ps-5 font-xssss text-grey-500 fw-500 border-light-md theme-dark-bg','placeholder':"What'son your mind?"}),
            
        }

class editProfile(forms.Form):
    
    p_img = forms.ImageField()
    
    
class add_MarketForm(forms.ModelForm):
    class Meta:
        model = Market
        fields = ['name','details','price','owner_type','pic1','pic2']
        widgets = {
            'name': forms.TextInput(attrs={'class':'form-control','placeholder':"Enter Name of the product"}),
            'price': forms.TextInput(attrs={'class':'form-control','placeholder':"Enter Price of the product"}),
            'owner_type': forms.TextInput(attrs={'class':'form-control','placeholder':"Second owner or first?"}),
            
            'details':  forms.Textarea(attrs={'class':'h100 bor-0 w-100 rounded-xxl p-2 ps-5 font-xssss text-grey-500 fw-500 border-light-md theme-dark-bg form-control','placeholder':"Enter details of the product"}),
            
        }