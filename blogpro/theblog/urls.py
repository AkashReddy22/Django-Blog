from django.contrib import admin
from django.urls import path
from .views import  home_page, login_page, register_page, new_post,my_posts,blog_detail_view,like_blog_view,logout
from .views import BlogPostListCreate, BlogPostDetail, CommentListCreate, CommentDetail, trending_blog_posts

urlpatterns = [
    path("home/", home_page, name='home_page'),   # Home page
    path("admin/", admin.site.urls),          # Admin interface
    path('login/', login_page, name='login_page'),    # Login page
    path('register/', register_page, name='register'),  # Registration page
    path('newpost/', new_post, name='new_post'),
    path('myblogs/',my_posts, name='my_blogs'),
    path('blog/<int:pk>/', blog_detail_view, name='blog_detail'),
    path('like/<int:pk>/', like_blog_view, name='like_blog'),
    path('logout/', logout, name='logout'),
    path('blogposts/', BlogPostListCreate.as_view(), name='blogpost-list-create'),
    path('blogposts/<int:pk>/', BlogPostDetail.as_view(), name='blogpost-detail'),
    path('comments/', CommentListCreate.as_view(), name='comment-list-create'),
    path('comments/<int:pk>/', CommentDetail.as_view(), name='comment-detail'),
    path('trending/', trending_blog_posts, name='trending-blogposts'),
]