from django.db import models
from auth_system.models import CustomUser
from django.core.validators import FileExtensionValidator
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User
from django.db import models
from auth_system.models import CustomUser
from django.utils import timezone


user_mode = (
    ('kids','kids'),
    ('teenager','teenager'),
    ('adult','adult'),
    ('general','general')
)

def validate_video_size(value):
    if value.size > 30 * 1024 * 1024:  # 20 MB limit
        raise ValidationError('The maximum file size allowed is 20 MB.')


class Post(models.Model):
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    video = models.FileField(upload_to='videos/', blank=True,null=True, validators=[FileExtensionValidator(allowed_extensions=['mp4', 'avi', 'mov']),validate_video_size])
    photo = models.ImageField(upload_to='photos/', blank=True,null=True)
    type = models.CharField(max_length=10,choices=user_mode,default='general')


class Advertisement(models.Model):
    content = models.TextField(blank=False)
    duration = models.IntegerField(blank=False)
    photo = models.ImageField(upload_to='photos/', blank=True,null=True)
    



class FriendList(models.Model):

	user 				= models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name="user")
	friends 			= models.ManyToManyField(CustomUser, blank=True, related_name="friends") 

	def __str__(self):
		return self.user.username

	def add_friend(self, account):
		"""
		Add a new friend.
		"""
		if not account in self.friends.all():
			self.friends.add(account)
			self.save()

	def remove_friend(self, account):
		"""
		Remove a friend.
		"""
		if account in self.friends.all():
			self.friends.remove(account)

	def unfriend(self, removee):
		"""
		Initiate the action of unfriending someone.
		"""
		remover_friends_list = self # person terminating the friendship

		# Remove friend from remover friend list
		remover_friends_list.remove_friend(removee)

		# Remove friend from removee friend list
		friends_list = FriendList.objects.get(user=removee)
		friends_list.remove_friend(remover_friends_list.user)


	def is_mutual_friend(self, friend):
		"""
		Is this a friend?
		"""
		if friend in self.friends.all():
			return True
		return False

request_mode = (
    ('accepted','accepted'),
    ('pending','pending'),
    ('declined','declined')
)
class FriendRequest(models.Model):
	"""
	A friend request consists of two main parts:
		1. SENDER
			- Person sending/initiating the friend request
		2. RECIVER
			- Person receiving the friend friend
	"""

	sender 				= models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="sender")
	receiver 			= models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="receiver")

	is_active			= models.BooleanField(blank=False, null=False, default=True)
	mode 				= models.CharField(max_length=10,choices=request_mode,default='pending')
	timestamp 			= models.DateTimeField(auto_now_add=True)

	def __str__(self):
		return self.sender.username

	def accept(self):
		"""
		Accept a friend request.
		Update both SENDER and RECEIVER friend lists.
		"""
		receiver_friend_list = FriendList.objects.get(user=self.receiver)
		if receiver_friend_list:
			receiver_friend_list.add_friend(self.sender)
			sender_friend_list = FriendList.objects.get(user=self.sender)
			if sender_friend_list:
				sender_friend_list.add_friend(self.receiver)
				self.is_active = False
				self.save()

	def decline(self):
		"""
		Decline a friend request.
		Is it "declined" by setting the `is_active` field to False
		"""
		self.is_active = False
		self.save()


	def cancel(self):
		"""
		Cancel a friend request.
		Is it "cancelled" by setting the `is_active` field to False.
		This is only different with respect to "declining" through the notification that is generated.
		"""
		self.is_active = False
		self.save()



class Market(models.Model):
	name = models.CharField(max_length=200,blank=False,null=False)
	seller = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
	details = models.CharField(max_length=900,blank=False)
	price = models.IntegerField()
	owner_type = models.CharField(max_length=20,blank=False,null=False)
	pic1 = models.ImageField(upload_to='photos/',blank=False,null=False)
	pic2 = models.ImageField(upload_to='photos/', blank=True,null=True)