from django.urls import path
from . import views

app_name = 'root'

urlpatterns = [
    path('',views.index,name='index'),
    path('my_profile/',views.my_profile,name='my_profile'),
    path('all_users/',views.all_users,name='all_users'),
    path('user_profile/<str:username>/',views.user_profile,name='user_profile'),
    path('notifications/',views.notifications,name='notifications'),
    path('display_video/<int:id>/',views.display_video,name='display_video'),
    path('kids/',views.kids,name='kids'),
    path('teenager/',views.teenager,name='teenager'),
    path('adult/',views.adult,name='adult'),
    path('my_friends/',views.my_friends,name='my_friends'),
    path('edit_profile/',views.edit_profile,name='edit_profile'),
    path('search/',views.search,name='search'),
    path('shop/',views.shop,name='shop'),
    path('sell_product/',views.sell_product,name='sell_product'),
    path('product_details/<int:id>/',views.product_details,name='product_details'),
    path('direct_msg_market/<int:secondId>/',views.direct_msg_market,name='direct_msg_market'),

    #for request and accept or confirm frd request
    path('send_friend_request/<str:username>/', views.send_friend_request, name='send_friend_request'),
    path('accept_friend_request/<int:sender_id>/', views.accept_friend_request, name='accept_friend_request'),
    #path('reject_friend_request/<int:request_id>/', views.reject_friend_request, name='reject_friend_request'),
]
