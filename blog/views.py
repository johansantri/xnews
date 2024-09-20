from django.shortcuts import render, get_object_or_404, redirect
from .models import Post, Comment, Category
from django.core.paginator import Paginator, EmptyPage,PageNotAnInteger
from .forms import CommentForm
from taggit.models import Tag
from django.db.models import Count
from django.db.models import Q
from django.db import connection
from django.views.generic import ListView, DetailView
from django.contrib.auth import login, authenticate 
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login, authenticate, logout, get_user_model #add this
from django.contrib.auth.forms import AuthenticationForm #add this
from .forms import SignUpForm 
from django.contrib import messages
from django.contrib.auth.models import User

def post_us(request):
    posts = User.objects.all()
    count = User.objects.all().count()
    
    query = request.GET.get('q')
    if query is not None and query !='':
        posts=User.objects.filter(Q(email__icontains=query) | Q(username__icontains=query)).distinct()  
        count = posts.count()     
    page = Paginator(posts,10)
    page_list = request.GET.get('page')
    page = page.get_page(page_list)
    
    context= {'count': count, 'page':page}

    return render(request,'blog/post_user.html',context)




class PostList(ListView):
    model = Post
    # paginate_by="5"
    queryset=Post.published.all()
    context_object_name = "posts"
    template_name = "blog/post_list.html"

def post_list(request, tag_slug=None,):
    posts = Post.published.all()
    
   #categori
    cursor = connection.cursor()
    cursor.execute('SELECT DISTINCT blog_category.category_text FROM blog_post JOIN blog_category ON blog_post.category_id=blog_category.id')
   
    po = cursor.fetchall()
    
  

     # post tag
    tag = None
    if tag_slug:
        tag = get_object_or_404(Tag, slug=tag_slug)
        posts = posts.filter(tags__in=[tag])
    
    # search
    query = request.GET.get("q")
    if query:
        posts=Post.published.filter(Q(title__icontains=query) | Q(tags__name__icontains=query)| Q(category__category_text__icontains=query)).distinct()
            
    paginator = Paginator(posts, 3) # 5 posts in each page
    page = request.GET.get('page')
    try:
        posts = paginator.page(page)

    except PageNotAnInteger:
        # If page is not an integer deliver the first page
        posts = paginator.page(1)
    except EmptyPage:
        # If page is out of range deliver last page of results
        posts = paginator.page(paginator.num_pages)
     
       
    return render(request,'blog/post_list.html',{'posts':posts, page:'pages', 'tag':tag,'po':po})
   


class PostDetail(DetailView):
    model = Post
    context_object_name = "post"
    template_name = "blog/post_detail.html"

def post_detail(request, post):
    post=get_object_or_404(Post,slug=post,status='published')
    cursor = connection.cursor()
    cursor.execute('SELECT DISTINCT blog_category.category_text FROM blog_post JOIN blog_category ON blog_post.category_id=blog_category.id')
   
    po = cursor.fetchall()
    # List of active comments for this post
    comments = post.comments.filter(active=True)
    new_comment = None

    if request.method == 'POST':
        # A comment was posted
        comment_form = CommentForm(data=request.POST)
        if comment_form.is_valid():
            # Create Comment object but don't save to database yet
            new_comment = comment_form.save(commit=False)
            # Assign the current post to the comment
            new_comment.post = post
            # Save the comment to the database
            new_comment.save()
            return redirect(post.get_absolute_url()+'#'+str(new_comment.id))
    else:
        comment_form = CommentForm()

    # List of similar posts
    post_tags_ids = post.tags.values_list('id', flat=True)
    similar_posts = Post.published.filter(tags__in=post_tags_ids).exclude(id=post.id)
    similar_posts = similar_posts.annotate(same_tags=Count('tags')).order_by('-same_tags','-publish')[:6]
    
    
    return render(request, 'blog/post_detail.html',{'post':post,'comments': comments,'comment_form':comment_form,'similar_posts':similar_posts,'po':po})

# handling reply, reply view
def reply_page(request):
    if request.method == "POST":

        form = CommentForm(request.POST)
        
        # print(form)

        if form.is_valid():
            post_id = request.POST.get('post_id')  # from hidden input
            parent_id = request.POST.get('parent')  # from hidden input
            post_url = request.POST.get('post_url')  # from hidden input

            #print(post_id)
           # print(parent_id)
           # print(post_url)


            reply = form.save(commit=False)
    
            reply.post = Post(id=post_id)
            reply.parent = Comment(id=parent_id)
            reply.save()

            return redirect(post_url+'#'+str(reply.id))

    return redirect("/")




def signup(request): 
    if request.user.is_anonymous:
        if request.method == "POST":
            form = SignUpForm(request.POST) 
            if form.is_valid(): 
                form.save() 
                username = form.cleaned_data.get('username') 
                password = form.cleaned_data.get('password1') 
                new_user = authenticate(username=username, password=password) 
                username = form.cleaned_data.get('username')
                messages.success(request, f'Account created for {username}!')
                if new_user is not None:
                    login(request, new_user) 
                    return redirect('/') 
    else:
        return redirect('/')
    form = SignUpForm()
    context = { 
            'form': form 
    } 
    return render(request, "auth/signup.html", context) 


def logout_request(request):
	logout(request)
	messages.info(request, "You have successfully logged out.") 
	return redirect('/')


def login_request(request):
	if request.method == "POST":
		form = AuthenticationForm(request, data=request.POST)
		if form.is_valid():
			username = form.cleaned_data.get('username')
			password = form.cleaned_data.get('password')
			user = authenticate(username=username, password=password)
			if user is not None:
				login(request, user)
				messages.info(request, f"You are now logged in as {username}.")
				return redirect('/')
			else:
				messages.error(request,"Invalid username or password.")
		else:
			messages.error(request,"Invalid username or password.")
	form = AuthenticationForm()
	return render(request=request, template_name="auth/login.html", context={"login_form":form})