from django.urls import path
from . import views
#from . import signup 
app_name = 'blog'
urlpatterns=[
    path('post_list/',views.post_list,name="post_list"),
    path('post_us/',views.post_us,name="post_user"),
    
    #path('signup/',views.signup, name='signup'), #this
    #path("logout/", views.logout_request, name= "logout"),
    #path("login/", views.login_request, name="login"),
    # path('<slug:slug>/',views.PostDetail.as_view(),name="post_detail"),
    path('<slug:post>/',views.post_detail,name="post_detail"),
    path('comment/reply/', views.reply_page, name="reply"),
    path('tag/<slug:tag_slug>/',views.post_list, name='post_tag'), #this
  
    #path('cat/<slug:tag_slug>/',views.post_list, name='post_tag'), #this
    

]