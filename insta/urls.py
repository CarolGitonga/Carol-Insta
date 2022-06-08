from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns=[
    path('', views.index, name='MainPage'),
    path('accounts/login', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
    path('profile/<username>', views.user_profile, name='profile'),
    path('<uuid:image_id>', views.single_image, name='singleImage'),
    path('add_image/', views.add_image, name='addImage'),
    path('profile/<username>/create', views.profile_form, name='createProfile'),
    path('profile/<username>/edit', views.profile_edit, name='editProfile'),
    path('<uuid:image_id>/like', views.like, name='likeImage'),
    path('search/', views.search_results, name='search_results'),
]

if settings.DEBUG:
    urlpatterns+= static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)