from django.urls import path
from . import views



urlpatterns = [path("", views.home, name="home"),
               path("about/", views.about, name="about"),
               path("contact/", views.contact, name="contact"),
               path("dashboard/", views.dashboard, name="dashboard"),
               path("login/", views.user_login, name = "login"),
               path("logout/", views.user_logout, name = "logout"),
               path("signup/", views.signup, name= "signup"),
               path("addpost/", views.add_post, name= "addpost"),
               path("updatepost/<int:id>", views.update_post, name= "updatepost"),
               path("delete/<int:id>", views.delete_post, name= "deletepost"),
               path("comment-blog/<int:id>/",views.Comment_Blog,name="comment-blog"),
               path("blog-detail/<int:id>/",views.Blog_Detail, name="blog-detail"),
               path("share-blog/<int:id>/",views.Share_Blog,name="share-blog"),
             path("search-blog/",views.search_blogs,name="search-blog"),
             ]