from django.urls import path
from . import views
#from . import signup 
app_name = 'blog'
urlpatterns=[
    path('blog/',views.blog,name="blog"),
    path('blog/add/',views.add,name="add"),
    path('post_list/',views.post_list,name="post_list"),
    path('post_us/',views.post_us,name="post_user"),
    path('<slug:post>/',views.post_detail,name="post_detail"),
    path('comment/reply/', views.reply_page, name="reply"),
    path('tag/<slug:tag_slug>/',views.post_list, name='post_tag'), #this
      

]