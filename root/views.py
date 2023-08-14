from django.shortcuts import render,redirect,get_object_or_404
from django.contrib.auth.decorators import login_required
from .forms import createPostForm,editProfile,add_MarketForm
from auth_system.models import CustomUser
from .models import FriendRequest,FriendList
from django.core.exceptions import ObjectDoesNotExist
from chat.models import Thread
from .models import Post,Advertisement,Market
from django.db.models import Q
# Create your views here.
@login_required(login_url='auth_system:login_user') 
def index(request):
    #for friend requests
    user = CustomUser.objects.get(id=request.user.id)
    try:
        friend_requests = FriendRequest.objects.filter(receiver=user,mode='pending')
    except ObjectDoesNotExist:
        friend_requests = None
    #for confirm friends
    user_profile = FriendList.objects.get(user=user)
    confirm_friends = user_profile.friends.all()
    #for random general post
    try:

        random_post = Post.objects.filter(type='general').order_by('?')[:15]
    except ObjectDoesNotExist:
        random_post = None
    print(random_post)
    form = createPostForm()
    if request.method == 'POST':
        form = createPostForm(request.POST,request.FILES)
        
        if form.is_valid():
            posttype = request.POST['postType']
            p = form.save(commit=False)
            if posttype:
                p.type = posttype
            p.user = request.user
            p.save()
            return redirect('root:my_profile')
        
        else:
            return render(request,'root/index.html',{'form':form})
    
    context ={
        'form':form,
        'friend_requests':friend_requests,
        'confirm_friends':confirm_friends,
        'random_post':random_post
        
    }
    return render(request,'root/index.html',context)

@login_required(login_url='auth_system:login_user')
def kids(request):
    #for random general post
    try:

        random_post_kids = Post.objects.filter(type='kids').order_by('?')[:20]
    except ObjectDoesNotExist:
        random_post_kids = None
    context={
        'random_post_kids':random_post_kids,
        'title':'Kids Page'
    }
    return render(request,'root/kids_page.html',context)

@login_required(login_url='auth_system:login_user')
def teenager(request):
    #for random general post
    try:

        random_post_teen = Post.objects.filter(type='teenager').order_by('?')[:20]
    except ObjectDoesNotExist:
        random_post_teen = None
    context={
        'random_post_kids':random_post_teen,
        'title':'Teenagers Page'
    }
    return render(request,'root/kids_page.html',context)

@login_required(login_url='auth_system:login_user')
def adult(request):
    #for random general post
    try:

        random_post_adult = Post.objects.filter(type='adult').order_by('?')[:20]
    except ObjectDoesNotExist:
        random_post_adult = None
    context={
        'random_post_kids':random_post_adult,
        'title':'Adults Page'
    }
    return render(request,'root/kids_page.html',context)

@login_required(login_url='auth_system:login_user')
def my_friends(request):
    user = CustomUser.objects.get(id=request.user.id)
    #for confirm friends
    user_profile = FriendList.objects.get(user=user)
    confirm_friends = user_profile.friends.all()
    context = {
        'all_users':confirm_friends,
        'cnt':confirm_friends.count()
    }
    return render(request,'root/my_friends.html',context)

@login_required(login_url='auth_system:login_user')
def edit_profile(request):
    user = CustomUser.objects.get(id=request.user.id)

    if request.method == 'POST':
        first_name = request.POST['first_name']
        
        contact = request.POST['contact']
        address = request.POST['address']
        about = request.POST['about']

        user = CustomUser.objects.get(id=request.user.id)
        user.first_name = first_name
        user.contact = contact
        user.address = address
        user.about = about
        user.save()

        return redirect('root:my_profile')

    context = {
        'user':user
    }
    return render(request,'root/edit_profile.html',context)

@login_required(login_url='auth_system:login_user')
def search(request):
    if request.method == 'POST':
        name = request.POST['inputsearch']
        lookups = Q(first_name__icontains=name)
        results = CustomUser.objects.filter(lookups).distinct()

        if results.exists():

            context = {
                            'found_users': results,
                            'r_count': results.count(),
                            
                        }
            return render(request, 'root/search_found.html', context)
        else:

            return render(request, 'root/search_not_found.html')
    context = {

    }
    return render(request,'root/search_found.html',context)

@login_required(login_url='auth_system:login_user')
def my_profile(request):
    
    user = request.user

    cobj = CustomUser.objects.get(id=user.id)
    if request.method == 'POST':
        
        print('jakljkdskfkdjf')
        form = editProfile(request.POST)     
        
        about = request.POST['about']
        cobj.about = about
        cobj.save()

        return redirect('root:my_profile')
    else:
        form = editProfile()

    #for post
    all_post = Post.objects.filter(user=user)[::-1]
    context = {
        'user':user,
        'form':form,
        'about_data':cobj.about,
        'all_post':all_post
    }
    return render(request,'root/my_profile.html',context)

@login_required(login_url='auth_system:login_user')
def display_video(request,id):
    post = Post.objects.get(id=id)
    advertisements = Advertisement.objects.all()
    user = CustomUser.objects.get(id=request.user.id)
    all_post = Post.objects.filter(type=user.mode).exclude(id=id)
    
    context={
        'post':post,
        'advertisements':advertisements,
        'all_post':all_post
    }
    return render(request,'root/display_video.html',context)

@login_required(login_url='auth_system:login_user')
def all_users(request):
    no_display_thisuser = ['admin',request.user.username]
    all_users = CustomUser.objects.exclude(username__in=no_display_thisuser)
    context ={
        'all_users':all_users
    }
    return render(request,'root/all_users.html',context)

@login_required(login_url='auth_system:login_user')
def user_profile(request,username):
    
    Send_on=False
    receiver_user = CustomUser.objects.get(username=username)
    user = CustomUser.objects.get(id=request.user.id)
    if user.username == username:
        return redirect('root:my_profile')
    
    try:
        try:
            pending_Request = FriendRequest.objects.filter(sender=receiver_user,receiver=user,mode='pending').first()
        except ObjectDoesNotExist:
            pending_Request = None
        if not pending_Request:
            Frequest  = FriendRequest.objects.filter(sender=user,receiver=receiver_user).first()
        else:
            Frequest = None

    except ObjectDoesNotExist:
        Frequest = None
    
    #####################

    try:
        alreadyf = FriendList.objects.filter(user=user,friends=receiver_user)
    except ObjectDoesNotExist:
        alreadyf = None
    
    all_post = Post.objects.filter(user=receiver_user)[::-1]
    
    context ={
        
        'r_user':receiver_user,
        'send_on':Send_on,
        'frequest':Frequest,
        'alreadyf':alreadyf,
        'pending_Request':pending_Request,
        'all_post':all_post
    }
    return render(request,'root/user_profile.html',context)


@login_required(login_url='auth_system:login_user')
def send_friend_request(request, username):
    receiver = CustomUser.objects.get(username=username)
    f_req = FriendRequest(sender=request.user,receiver=receiver,mode='pending')
    f_req.save()
    return redirect('root:user_profile', username=username)


@login_required(login_url='auth_system:login_user')
def accept_friend_request(request, sender_id):
    
    user = CustomUser.objects.get(id=request.user.id)
    frequest_obj = FriendRequest.objects.get(id=sender_id)
    # frequest_obj = FriendRequest.objects.get(sender=sender_obj,receiver=user,mode='pending')
    sender_obj = CustomUser.objects.get(id=frequest_obj.sender.id)
    frequest_obj.mode='accepted'
    frequest_obj.accept()
    frequest_obj.save()
    

    #now create thread object for messages
    Thread.objects.create(first_person = sender_obj,second_person=user)


    return redirect('root:user_profile', username=sender_obj.username)


@login_required(login_url='auth_system:login_user')
def notifications(request):
    user = CustomUser.objects.get(id=request.user.id)
    try:
        friend_requests = FriendRequest.objects.filter(receiver=user,mode='pending')
    except ObjectDoesNotExist:
        friend_requests = None

    context ={
        'friend_requests':friend_requests
    }
    return render(request,'root/notification.html',context)

@login_required(login_url='auth_system:login_user')
def shop(request):
    all = Market.objects.all()[:]
    cnt = all.count()
    context ={
        'all':all,
        'cnt':cnt
    }
    return render(request,'root/shop.html',context)

@login_required(login_url='auth_system:login_user')
def sell_product(request):

    
    if request.method == 'POST':
        form = add_MarketForm(request.POST,request.FILES)
        
        if form.is_valid():
            p = form.save(commit=False)
            user = CustomUser.objects.get(id=request.user.id)
            p.seller = user
            p.save()
            return redirect('root:shop')
        
        else:
            return redirect('root:sell_product')
    else:
        form = add_MarketForm()


    context ={
        'form':form
    }
    return render(request,'root/sell_product.html',context)

@login_required(login_url='auth_system:login_user')
def product_details(request,id):
    product = Market.objects.get(id=id)

    receiver_user = CustomUser.objects.get(id=product.seller.id)
    user = CustomUser.objects.get(id=request.user.id)
    try:
        alreadyf = FriendList.objects.filter(user=user,friends=receiver_user)
    except ObjectDoesNotExist:
        alreadyf = None
    context ={
        'product':product,
        'alreadyf':alreadyf
    }
    return render(request,'root/product_details.html',context)

@login_required(login_url='auth_system:login_user')
def direct_msg_market(request,secondId):
    sender_obj = CustomUser.objects.get(id=request.user.id)
    s_user = CustomUser.objects.get(id=secondId)
    #now create thread object for messages
    Thread.objects.create(first_person = sender_obj,second_person=s_user)

    return redirect('chat:messages_page')