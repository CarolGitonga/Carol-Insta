from django.test import TestCase
from .models import Image,Profile,Likes,Comments
from django.contrib.auth.models import User
import datetime as dt

# Create your tests here.
class ProfileTestCase(TestCase):
    def setUp(self):
        user = User.objects.create_user(username='carol', password='12345')
        
        Profile.objects.create(user=user, location='Kenya', bio='my bio', avatar='image.jpg')
        
        self.location = Profile(location='Kenya')
        
    def test_instance(self):
        self.assertTrue(isinstance(self.location,Profile))

class TestImage(TestCase):
    def setUp(self):
        user = User.objects.create_user(username='carol', password='12345')
        profile = Profile.objects.create(user=user, location='Kenya', bio='my bio', avatar='image.jpg')
        self.image_test = Image(user=user, image='image.jpg', image_name='NationalPark', caption='Nairobi', date='2021-09-04 06:00:00.000000-08:00', profile=profile, like=10)

    def test_instance(self):
        self.assertTrue(isinstance(self.image_test, Image))

    def test_save_post(self):
        self.image_test.save_image()
        after = Image.objects.all()
        self.assertTrue(len(after) > 0)

    def test_delete_image(self):
        self.image_test.delete_image()
        images = Image.objects.all()
        self.assertTrue(len(images) == 0)

    def test_update_image(self):
        self.image_test.save_image()
        self.image_test.update_caption(self.image_test.id, 'test work')
        changed_img = Image.objects.filter(caption='test work')
        self.assertTrue(len(changed_img) > 0)

    def tearDown(self):
        Image.objects.all().delete()

class LikesTestCase(TestCase):
    def setUp(self):
        user = User.objects.create_user(username='carol', password='12345')
        profile = Profile.objects.create(user=user, location='Kenya', bio='my bio', avatar='image.jpg')
        image = Image.objects.create(user=user, image='image.jpg', image_name='Nationalpark', caption='Nairobi', date='2021-09-04 06:00:00.000000-08:00', profile=profile, like=10)
        
        Likes.objects.create(user=user, image=image)
        
        self.user = Likes(user=user)
        
    def test_instance(self):
        self.assertTrue(isinstance(self.user,Likes))

class CommentsTestCase(TestCase):
    def setUp(self):
        user = User.objects.create_user(username='carol', password='12345')
        profile = Profile.objects.create(user=user, location='Kenya', bio='my bio', avatar='image.jpg')
        image = Image.objects.create(user=user, image='image.jpg', image_name='NationalPark', caption='Nairobi', date='2021-09-04 06:00:00.000000-08:00', profile=profile, like=10)
        
        Comments.objects.create(comments='its testing!!!', user=user, date='2021-09-04 06:00:00.000000-08:00', image=image)
        self.comments = Comments(comments='its testing!!!')
        
    def test_instance(self):
        self.assertTrue(isinstance(self.comment,Comments))


