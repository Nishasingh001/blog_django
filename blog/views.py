from django.shortcuts import render, HttpResponseRedirect
from django.http import HttpResponse,HttpResponseNotFound
from django.shortcuts import render, redirect
from django.views import View
from django.views.generic import ListView
from .models import (    
    Post,
    Comment,
    Share_post
    )
from datetime import datetime
from django.contrib.auth.models import User,Group
from .forms import SignupForm,LoginForm, PostForm
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from . email import  share_blog
from django.db.models import Q
import uuid


def signup(request):
    if request.method == 'POST':
        fm = SignupForm(request.POST)
        if fm.is_valid():
            messages.success(request, "Account created successfully !!!")
            user = fm.save()
            group = Group.objects.get(name ='Author')
            user.groups.add(group)
    else:
        fm = SignupForm()
    return render(request, 'signup.html', {'form':fm})

def user_login(request):
    if not request.user.is_authenticated:
        if request.method == 'POST':
            fm = LoginForm(request =request, data = request.POST)
            if fm.is_valid():
                username =  fm.cleaned_data['username']
                pwd = fm.cleaned_data['password']
                user = authenticate(username = username, password = pwd)
                if user is not None:
                    login(request,user)
                    messages.success(request, "Logged in successfully")
                    return HttpResponseRedirect('/dashboard/')
        else:
            fm = LoginForm()
        return render(request, 'login.html', {'form':fm})
    else:
        return HttpResponseRedirect('/dashboard/')


def user_logout(request):
    logout(request)
    return HttpResponseRedirect('/')

def home(request):
    posts =Post.objects.all()
    return render(request, "home.html", {"posts":posts})

def about(request):
    return render(request, "about.html")

def dashboard(request):
    if request.user.is_authenticated:
        posts =Post.objects.all()
        user = request.user
        full_name = user.get_full_name()
        gps = user.groups.all()
        return render(request, "dashboard.html", {'posts':posts,'name':full_name,'groups':gps})
    else:
        return HttpResponseRedirect('/login/')    
    
def contact(request):
    return render(request, "contact.html")

def add_post(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            fm = PostForm(request.POST)
            if fm.is_valid():
                title =  fm.cleaned_data['title']
                content = fm.cleaned_data['content']  
                pst = Post(title=title, content=content, created_at = datetime.now())  
                pst.save() 
                fm = PostForm()  
        else:
            fm = PostForm() 
        return render(request, "add_post.html",{"fm":fm})
    else:
        return HttpResponseRedirect('/login/')    
    
def update_post(request,id):
    if request.user.is_authenticated: 
        if request.method == 'POST':
            pi = Post.objects.get(pk=id)
            fm = PostForm(request.POST, instance=pi)
            if fm.is_valid(): 
                fm.save()
        else:
            pi = Post.objects.get(pk=id)
            fm = PostForm(instance=pi)
        return render(request, "update_post.html", {"fm":fm})
    else:
        return HttpResponseRedirect('/login/') 

def delete_post(request,id):
    if request.user.is_authenticated: 
        if request.method == 'POST':
            pi = Post.objects.get(pk=id)
            pi.delete()      
            return HttpResponseRedirect('/dashboard/') 
    else:
        return HttpResponseRedirect('/login/')  


@login_required(login_url='login')
def Comment_Blog(request,id):
    obj = Post.objects.get(id=id)
    if request.method == 'POST':
        comment = request.POST.get("comment")
        email = request.POST.get("email")
        user = request.user        
        comment_obj = Comment.objects.create(post = obj, author = user, email=email, comment=comment)
        detail_page_url = reverse('blog-detail', args=[obj.id])
        
        return redirect(detail_page_url)   
    

@login_required(login_url='login')
def Blog_Detail(request,id):
    obj = Post.objects.get(id = id)
    comment = Comment.objects.filter(post= id)
    context = {
        "response": obj,
        "comment" : comment
    }
    return render (request,'blog_detail.html',context)

@login_required(login_url='login')
def Share_Blog(request,id):
    obj = Post.objects.get(id = id)
    if request.method == "POST":
        comment = request.POST.get("comment")
        name = request.POST.get("name")
        email_f = request.POST.get("email")
        to = request.POST.get("to")
        user = request.user 
        blog_token = Share_post.objects.create(blog=obj, email = to, token = uuid.uuid4())
        share_blog(email_f,obj.title,to,comment,blog_token.token,name)
        commnet_obj = Comment.objects.create(post = obj, author = user, email=email_f,comment=comment)
        return HttpResponse("Your Post has shared check your email")

    context = {
        "response": obj,
    }

    return render(request,"share_blog.html",context)

@login_required(login_url='login')
def search_blogs(request):
    query = request.POST.get('query')
    print("---------------------",query)
    if query:
        # Perform a case-insensitive search for each word in the query
        query_list = query.split()
        blogs = Post.objects.filter(
            Q(title__icontains=query) |
            Q(content__icontains=query)|
            Q(hashtags__hashtag__in=query_list)
        ).distinct()
    else:
        blogs = Post.objects.none()  # Return no results if no query is provided

    context = {
        "response": blogs
    }
    return render(request, 'blog_detail.html', context)
    

