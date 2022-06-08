import uuid
from django.db import models
from django.contrib.auth.models import User
from cloudinary.models import CloudinaryField

# Create your models here.
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    location = models.CharField(max_length=50, null=True, blank=True)
    bio = models.TextField(max_length=120, null=True)
    avatar = CloudinaryField('image')

    def __str__(self):
        return self.bio

    def save_image(self):
        self.save()
        
    def delete_image(self):
        self.delete()
    
    @classmethod
    def update(cls, id, value):
        cls.objects.filter(id=id).update(avatar=value)


class Image(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='image_user')
    image = CloudinaryField('image')
    image_name = models.CharField(max_length=120, null=True)
    caption = models.TextField(max_length=1000, verbose_name='Caption', null=True)
    date = models.DateTimeField(auto_now_add=True)
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='image_profile')
    like = models.IntegerField(default=0)
    
    
    def __str__(self):
        return self.image_name
    
    def save_image(self):
        self.save()
        
    @classmethod
    def search_user(cls,search_term):
        users = User.objects.filter(username__icontains=search_term)
        return users
        
    def delete_image(self):
        self.delete()
    
    @classmethod
    def update_caption(cls, id, value):
        cls.objects.filter(id=id).update(caption=value)


class Comments(models.Model):
    comments = models.TextField(null=True)
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='user_comments')
    date = models.DateTimeField(auto_now_add=True)
    image = models.ForeignKey(Image, on_delete=models.CASCADE, related_name='image_comments')

class Likes(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_like')
    image = models.ForeignKey(Image, on_delete=models.CASCADE, related_name='image_like')
