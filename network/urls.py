from django.conf import settings
from django.conf.urls.static import static
from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),

    
    path("profile/<str:username>", views.profile, name="profile"),
    path("follow/<str:username>", views.follow, name="follow"),
    path("unfollow/<str:username>", views.unfollow, name="unfollow"),
    path("following", views.following, name="following"),
    
    path("new_post", views.new_post, name="new_post"),
    path("post/<int:post_id>", views.post, name="post"),
    path("edit_post/<int:post_id>", views.edit_post, name="edit_post"),
     path("like_post/<int:post_id>", views.like_post, name="like_post"),

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
