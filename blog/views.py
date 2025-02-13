from django.shortcuts import render, redirect, get_object_or_404
from .forms import BlogForm
from .models import Blog 
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

@login_required(login_url='login')  
def home(request):
    if request.method == 'POST':
        form = BlogForm(request.POST, request.FILES) 
        if form.is_valid():  
            blog = form.save()   

            if request.user.is_authenticated:
                blog.created_by = request.user
            blog.save() 
            return redirect('home')
    else:
        form = BlogForm() 
    if request.user.is_superuser:
        blogs=Blog.objects.all()
    else:
        blogs = Blog.objects.filter(created_by=request.user)    # When using the filter, pass the request.user and created_by is used from the table.
    return render(request, 'home.html', {'form': form, 'blogs': blogs})

def user_logout(request):
    logout(request)
    messages.success(request, "Successfully Logged Out")
    return redirect('login')

def user_signup(request):
    if request.method == 'POST':
        Username1 = request.POST['Username1']
        Name1 = request.POST['Name1']
        Email1 = request.POST['Email1']
        Password1 = request.POST['Password1']
        Confirmpassword1 = request.POST['Confirmpassword1']

        if User.objects.filter(username=Username1).first(): 
            messages.error(request, "User already exists")
            return redirect('/login')

        if Password1 != Confirmpassword1:
            messages.error(request, "Please match your Password")
            return redirect('signup/')

        # Create user
        try:
            myuser = User.objects.create_user(Username1, Email1, Password1)
            myuser.first_name = Name1
            myuser.save()
            messages.success(request, "Your account has been created successfully")
            return redirect('/login')

        except Exception as e:
            messages.error(request, f"Error creating user: {e}")
            return render(request, 'signup.html')

    else:
        return render(request, 'signup.html')

def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('UserName1')
        password = request.POST.get('Password1')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            messages.success(request, "Successfully Logged In")
            return redirect('home') 
        else:
            messages.error(request, "Invalid Credentials")
            return render(request, 'login.html')
    return render(request, 'login.html')

def edit(request, blog_id):
    if request.user.is_superuser:
        blog = get_object_or_404(Blog, pk=blog_id)
    else:
        blog = get_object_or_404(Blog, pk=blog_id, created_by=request.user)
    
    if request.method == 'POST':
        form = BlogForm(request.POST, request.FILES, instance=blog) 
        if form.is_valid():
            form.save()
            messages.success(request, "Blog post updated successfully!")
            return redirect('home') 
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        form = BlogForm(instance=blog)

    return render(request, 'edit.html', {'form': form, 'blog': blog})

def delete(request,blog_id):
    blog = get_object_or_404(Blog, id=blog_id)
    blog.delete()
    messages.success(request, 'Your Blog has been Deleted Successfully!')
    return redirect("/") 

   








