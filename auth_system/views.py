from django.shortcuts import render,redirect
from .forms import registerUser,loginUser
from django.contrib.auth import authenticate,login,logout
from django.contrib import messages
import socket
from django.utils.safestring import mark_safe
from django.core.mail import send_mail, BadHeaderError
from django.http import HttpResponse
from django.contrib.auth.forms import PasswordResetForm
from root.models import FriendRequest,FriendList
from django.template.loader import render_to_string
from django.db.models.query_utils import Q
from django.utils.http import urlsafe_base64_encode
from django.contrib.auth.tokens import default_token_generator
from django.utils.encoding import force_bytes
from .models import CustomUser
from django.conf import settings
#email
from django.core.mail import EmailMessage
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from django.template.loader import get_template,render_to_string
from django.utils import timezone
import datetime
# Create your views here.
def login_user(request):
    
    form = loginUser()
    err = 0
    if request.method == 'POST':
        
        username = request.POST['username']
        password = request.POST['password']
    
        user = authenticate(request,username=username,password = password)
        
        if user is not None:
            login(request, user)
            
            return redirect('root:index') 
            
        else:
            messages.error(request,'Username or Password not correct')
            return render(request,'auth_system/login.html',{'form':form})
    context = {
            'form':form
    }
    return render(request,'auth_system/login.html',context)

def register_user(request):
    form = registerUser()
    if request.method == 'POST':
        form = registerUser(request.POST,request.FILES)
        
        if form.is_valid():
            p = form.save(commit=False)

            today = datetime.date.today()
            
            b_date = request.POST['b_date']
            b_year = b_date[0:4]
            b_mo = b_date[5:7]
            b_day = b_date[8:]

            #age = today.year - birthdate.year - ((today.month, today.day) < (birthdate.month, birthdate.day))
            age = today.year - int(b_year) - ((today.month, today.day) < (int(b_mo), int(b_day)))
            p.age = age

            if age <=10 :
                p.mode = 'kid'
            elif age > 10 and age <20:
                p.mode = 'teenager'
            elif age > 20:
                p.mode = 'adult'

            
            p.save()
            a= CustomUser.objects.get(id=p.id)
            #for friendlist add
            frdlist = FriendList(user=a)
            frdlist.save()

            #!reply as email to registered person
            flag = ''
            try:
                # connect to the host -- tells us if the host is actually
                # reachable
                socket.create_connection(("1.1.1.1", 53))
                flag='net_on'
            except OSError:
                flag='net_off'
            #reply as email to contected person
            e_tmp = 'root/email_registeredonsite.html'
            c = {'name':p.first_name}
            content = render_to_string(e_tmp,c)
            img_data = open('static/images/logo2.png', 'rb').read()
            html_part = MIMEMultipart(_subtype='related')
            body = MIMEText(content, _subtype='html')
            html_part.attach(body)
            # Now create the MIME container for the image
            img = MIMEImage(img_data, 'png')
            img.add_header('Content-Id', '<myimage>')  # angle brackets are important
            img_data2 = open('static/images/logo2.png', 'rb').read()
            img2 = MIMEImage(img_data2, 'jpg')
            img2.add_header('Content-Id', '<myimage2>')  # angle brackets are important
            # img.add_header("Content-Disposition", "inline", filename="myimage") # David Hess recommended this edit
            html_part.attach(img)
            html_part.attach(img2)
            to_mail = p.email
            msg = EmailMessage("You are registered on Protubeweb ", None,  settings.EMAIL_HOST_USER,  [to_mail])
            msg.attach(html_part) # Attach the raw MIMEBase descendant. This is a public method on EmailMessage
            if flag == 'net_on':
                msg.send()
            else:
                print('network is not on')


            return redirect('auth_system:login_user') #loginpage
            
        else:
            # messages.info(request,mark_safe('1. Email must be in format like tmp@gmail.com <br/>2. Password Contains at list 8 character, alphabets and specials'))
            return render(request,'Auth_system/register.html',{'form':form})
    
    context = {
        'form':form
    }
    return render(request,'auth_system/register.html',context)


def logout_user(request):
    logout(request)

    return redirect('auth_system:login_user')




def password_reset_request(request):
	if request.method == "POST":
		password_reset_form = PasswordResetForm(request.POST)
		if password_reset_form.is_valid():
			data = password_reset_form.cleaned_data['email']
			associated_users = CustomUser.objects.filter(Q(email=data))
			if associated_users.exists():
				for user in associated_users:
					subject = "Password Reset Requested"
					email_template_name = "auth_system/password_reset.txt"
					c = {
					"email":user.email,
					'domain':'127.0.0.1:8000',
					'site_name': 'Website',
					"uid": urlsafe_base64_encode(force_bytes(user.pk)),
					"user": user,
					'token': default_token_generator.make_token(user),
					'protocol': 'http',
					}
					email = render_to_string(email_template_name, c)
					try:
                        
						send_mail(subject, email, settings.EMAIL_HOST_USER , [user.email], fail_silently=False)
					except BadHeaderError:
						return HttpResponse('Invalid header found.')
                    
					return redirect("auth_system:password_reset_done")
	password_reset_form = PasswordResetForm()
	return render(request=request, template_name="auth_system/password_reset.html", context={"password_reset_form":password_reset_form})