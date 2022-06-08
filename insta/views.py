from django.shortcuts import render, HttpResponseRedirect, redirect, get_object_or_404
from django.http import HttpResponse, Http404,HttpResponseRedirect
import datetime as dt
from .forms import *
from .models import *
from .email import send_welcome_email
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login
from django.contrib.auth import logout as django_logout
from django.urls import reverse



# Create your views here.
def index(request):
    images = Image.objects.all()
    return render(request, 'index.html', {'images':images})


def login(request):
    username = request.IMAGE['username']
    password = request.IMAGE['password']
    user = authenticate(request, username=username, password=password)
    if user is not None:
        login(request, user)
        return redirect(request,'/')
    
    return render(request, '/django_registration/login.html')
        
@login_required
def logout(request):
    django_logout(request)
    return  HttpResponseRedirect('/')


@login_required
def user_profile(request, username):
    user = get_object_or_404(User, username=username)
    profile = Profile.objects.get(user=user)
    avatar = Profile.objects.all()
    images = Image.objects.filter(user=user).order_by("-date")
    image_count = Image.objects.filter(user=user).count()
  
    
    return render(request,'profile/profile.html', {'user':user, 'profile':profile, 'images':images, 'avatar':avatar, 'image_count':image_count, })


@login_required
def single_image(request,image_id):
    image = get_object_or_404(Image, id=image_id)
    user = request.user
    profile = get_object_or_404(Profile, user=user)
    comments = Comments.objects.filter(image=image).order_by('-date')
    
    if request.method == "POST":
        form = CommentsForm(request.POST)
        if form.is_valid():
            data = form.save(commit=False)
            data.profile = profile
            data.image = image
            data.save()
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
            #return redirect('singleImage')
        else:
            form = CommentsForm()
    
    return render(request, 'single_image.html', {'image':image, 'form':CommentsForm, 'comments':comments})

@login_required
def add_image(request):
    userX = request.user
    user = Profile.objects.get(user=request.user)
    if request.method == "POST":
        form = ImageForm(request.POST, request.FILES)
        if form.is_valid():
            image = form.save(commit=False)
            image.profile = user
            image.user = userX
            image.save()
            return redirect('')
        else:
            return False
    
    return render(request, 'add_image.html', {'userX':userX,'form':ImageForm,}) 

@login_required
def profile_form(request,username):
    userX = request.user
    user = get_object_or_404(User, username=username)
    if request.method == "POST":
        form = ProfileForm(request.POST, request.FILES)
        if form.is_valid():
            data = form.save(commit=False)
            data.user = userX
            data.save()
            return HttpResponseRedirect(reverse('MainPage'))
        else:
            form = ProfileForm()
    legend = 'Create Profile'
    
    return render(request, 'profile/update_profile.html', {'form':ProfileForm, 'legend':legend, 'user':user, 
                                                   'userX':userX})


@login_required
def profile_edit(request,username):
    user = get_object_or_404(User, username=username)
    profile = user.profile
    form = EditProfileForm(instance=profile)
    
    if request.method == "POST":
        form = EditProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            data = form.save(commit=False)
            data.user = user
            data.save()
            return HttpResponseRedirect(reverse('profile', args=[username]))
        else:
            form = EditProfileForm(instance=profile)
    legend = 'Edit Profile'
    return render(request, 'profile/update_profile.html', {'legend':legend, 'form':ProfileForm})


@login_required
def like(request,image_id):
    user = request.user
    image = Image.objects.get(id=image_id)
    current_likes = image.like
    
    liked = Likes.objects.filter(user=user, image=image).count()
    
    if not liked:
        like = Likes.objects.create(user=user,image=image)
        
        current_likes = current_likes + 1
        
    else:
        Likes.objects.filter(user=user,image=image).delete()
        current_likes = current_likes - 1
        
    image.like = current_likes
    image.save() 
    
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))  


def search_results(request):
    
    if "users" in request.GET and request.GET["users"]:
        search_term = request.GET.get("users")
        searched_accounts = Image.search_user(search_term)
        message = f"{search_term}"

        return render(request, 'search.html',{"message":message,"users": searched_accounts})

    else:
        message = "You haven't searched for any user"
        return render(request, 'search.html',{"message":message}) 