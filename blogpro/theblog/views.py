from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import logout as auth_logout
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from .models import BlogPost, Comment
from .serializers import BlogPostSerializer, CommentSerializer
from rest_framework.decorators import api_view
from rest_framework.response import Response


from django.contrib.auth.models import User
from .models import *

# Create your views here.
def login_page(request):
    # Check if the HTTP request method is POST (form submission)
    print(request.method)

    if request.method == 'POST':
        
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            return redirect('/home/')  # Redirect to a homepage or dashboard
        else:
            messages.error(request, 'Invalid username or password.')
    return render(request, 'login.html')

def register_page(request):
    # Check if the HTTP request method is POST (form submission)
    if request.method == 'POST':
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        username = request.POST.get('username')
        password = request.POST.get('password')
         
        # Check if a user with the provided username already exists
        user = User.objects.filter(username=username)
         
        if user.exists():
            # Display an information message if the username is taken
            messages.info(request, "Username already taken!")
            return redirect('/register/')
         
        # Create a new User object with the provided information
        user = User.objects.create_user(
            first_name=first_name,
            last_name=last_name,
            username=username
        )
         
        # Set the user's password and save the user object
        user.set_password(password)
        user.save()
         
        # Display an information message indicating successful account creation
        messages.info(request, "Account created Successfully!")
        return redirect('/login/')
     
    # Render the registration page template (GET request)
    return render(request, 'register.html')

@login_required
def home_page(request):
    # RETRIEVE ALL POSTS FROM DATABASE
    posts = BlogPost.objects.all()

    return render(request, 'home.html', {'blogs': posts})

@login_required
def my_posts(request):
    # RETRIEVE ALL POSTS FROM DATABASE BY THE CURRENT USER
    posts = BlogPost.objects.filter(author=request.user)

    return render(request, 'myblogs.html', {'blogs': posts})


@login_required
def new_post(request):
    if request.method == 'POST':
        print(request)
        print(request.POST)
        title = request.POST.get('title')
        body = request.POST.get('body')

        new_post = BlogPost.objects.create(author=request.user, title=title, body=body )
        print(new_post)

        return redirect('/home/')

    return render(request, 'newpost.html')

@login_required
def blog_detail_view(request, pk):
    blog = get_object_or_404(BlogPost, pk=pk)
    if request.method == 'GET' and request.user != blog.author:
        blog.views += 1
        blog.save()

    if request.method == 'POST':
        comment_text = request.POST.get('comment_text')
        if comment_text:
            comment = Comment.objects.create(blog_post=blog, author=request.user, comment_text=comment_text)
            messages.success(request, 'Comment added successfully')
            return redirect('blog_detail', pk=pk)
    return render(request, 'blog_detail.html', {'blog': blog})

@login_required
def like_blog_view(request, pk):
    blog = get_object_or_404(BlogPost, pk=pk)
    if blog.likes.filter(id=request.user.id).exists():
        blog.likes.remove(request.user)
    else:
        blog.likes.add(request.user)
    return redirect('blog_detail', pk=pk)

@login_required
def logout(request):
    auth_logout(request)  # Call the auth_logout function to.logout(request)
    return render(request, 'logout.html')

# BlogPost Views
class BlogPostListCreate(APIView):
    def get(self, request):
        blog_posts = BlogPost.objects.all()
        serializer = BlogPostSerializer(blog_posts, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = BlogPostSerializer(data=request.data)
        print(serializer)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class BlogPostDetail(APIView):
    def get(self, request, pk):
        blog_post = get_object_or_404(BlogPost, pk=pk)
        serializer = BlogPostSerializer(blog_post)
        return Response(serializer.data)

    def put(self, request, pk):
        blog_post = get_object_or_404(BlogPost, pk=pk)
        serializer = BlogPostSerializer(blog_post, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, pk):
        blog_post = get_object_or_404(BlogPost, pk=pk)
        serializer = BlogPostSerializer(blog_post, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        blog_post = get_object_or_404(BlogPost, pk=pk)
        blog_post.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

# Comment Views
class CommentListCreate(APIView):
    def get(self, request):
        comments = Comment.objects.all()
        serializer = CommentSerializer(comments, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = CommentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class CommentDetail(APIView):
    def get(self, request, pk):
        comment = get_object_or_404(Comment, pk=pk)
        serializer = CommentSerializer(comment)
        return Response(serializer.data)

    def put(self, request, pk):
        comment = get_object_or_404(Comment, pk=pk)
        serializer = CommentSerializer(comment, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, pk):
        comment = get_object_or_404(Comment, pk=pk)
        serializer = CommentSerializer(comment, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        comment = get_object_or_404(Comment, pk=pk)
        comment.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

# Trending Blog Posts
@api_view(['GET'])
def trending_blog_posts(request):
    blog_posts = BlogPost.objects.all()
    blog_posts = sorted(blog_posts, key=lambda x: x.views + x.likes.count() * 2 + x.comments.count() * 3, reverse=True)
    serializer = BlogPostSerializer(blog_posts, many=True)
    return Response(serializer.data)
